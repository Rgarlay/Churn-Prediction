import os


class s3Sync:
    def sync_folder_to_s3(self, folder,aws_s3_bucket_url):
        command = f"aws s3 sync {folder} {aws_s3_bucket_url}"
        os.system(command)
    
    def sync_folder_from_s3(self, folder, aws_s3_bucet_url):
        command = f"aws s3 sync {aws_s3_bucet_url} {folder}"
        os.system(command)