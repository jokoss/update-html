import os
import shutil

def main():
    # List of template files to remove
    template_files = [
        'MotzzWebsite-main/landing-saas-v1.html',
        'MotzzWebsite-main/landing-saas-v2.html',
        'MotzzWebsite-main/services-v1.html',
        'MotzzWebsite-main/services-single-v1.html'
    ]
    
    # Create a backup directory
    backup_dir = 'template_backup'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Move files to backup directory
    for file_path in template_files:
        if os.path.exists(file_path):
            # Get the filename without the directory
            filename = os.path.basename(file_path)
            # Copy the file to the backup directory
            shutil.copy2(file_path, os.path.join(backup_dir, filename))
            # Remove the original file
            os.remove(file_path)
            print(f"Moved {file_path} to {backup_dir}/{filename}")
        else:
            print(f"File {file_path} does not exist")

if __name__ == "__main__":
    main()
