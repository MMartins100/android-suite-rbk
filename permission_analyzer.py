import sys
import os
from androguard.core.bytecodes.apk import APK

class PermissionAnalyzer:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.permissions = []

    def analyze(self):
        # Check if the file exists
        if not os.path.isfile(self.apk_path):
            print(f"Error: {self.apk_path} does not exist.")
            return

        # Extract permissions using androguard
        try:
            apk = APK(self.apk_path)
            self.permissions = apk.get_permissions()
        except Exception as e:
            print(f"Error: Unable to parse APK file. {e}")
            return

        # Display extracted permissions
        self.display_permissions()

    def extract_permissions(self, manifest_path):
        # This method is no longer needed with androguard
        return self.permissions

    def display_permissions(self):
        # Print the permissions in a user-friendly format
        if not self.permissions:
            print("No permissions found in the APK.")
            return
        
        print(f"Permissions for {self.apk_path}:")
        for perm in self.permissions:
            print(f"- {perm}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python permission_analyzer.py <path_to_apk>")
        sys.exit(1)

    apk_path = sys.argv[1]
    analyzer = PermissionAnalyzer(apk_path)
    analyzer.analyze()
