

def test_upload_file(login):
    login.create_project()
    login.find_project(login.project_name)
    login.upload_file_to_project()
    assert login.uploaded_file
