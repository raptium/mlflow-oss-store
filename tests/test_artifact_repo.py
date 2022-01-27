from mlflow_oss.artifact_repo import OSSArtifactRepository
import tempfile

import os

test_bucket = os.environ['MLFLOW_OSS_TEST_BUCKET']


def test_log_and_download():
    repo = OSSArtifactRepository("oss://%s/test" % test_bucket)
    tmpf = tempfile.mktemp(suffix=".txt")
    with open(tmpf, "w+") as f:
        f.write("hello")
    repo.log_artifact(tmpf, "/")

    tmpf2 = tempfile.mktemp(suffix=".txt")
    repo._download_file(os.path.basename(tmpf), tmpf2)
    with open(tmpf2, "r") as f:
        assert f.read() == "hello"


def test_log_directory():
    repo = OSSArtifactRepository("oss://%s/test" % test_bucket)
    tmpdir = tempfile.mkdtemp()
    with open(os.path.join(tmpdir, "hello1.txt"), "w+") as f:
        f.write("hello")
    with open(os.path.join(tmpdir, "hello2.txt"), "w+") as f:
        f.write("hello")
    os.makedirs(os.path.join(tmpdir, "subdir"))
    with open(os.path.join(tmpdir, "subdir", "hello3.txt"), "w+") as f:
        f.write("hello")
    repo.log_artifacts(tmpdir, "/artifacts")

    artifacts = repo.list_artifacts("/artifacts/")
    assert len(artifacts) == 3

    artifacts = repo.list_artifacts("/artifacts/not-found")
    assert len(artifacts) == 0
