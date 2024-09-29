# Navigate to the root directory of your Git repository
cd "C:\path\to\your\repository"

# Remove the __pycache__ directories
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | ForEach-Object {
    Remove-Item -Recurse -Force -Path $_.FullName
}

# Remove *.pyc and *.log files
Get-ChildItem -Recurse -Filter "*.pyc" | ForEach-Object {
    Remove-Item -Force -Path $_.FullName
}
Get-ChildItem -Recurse -Filter "*.log" | ForEach-Object {
    Remove-Item -Force -Path $_.FullName
}

# Remove environment folders (.env, .venv, venv, ENV)
$envFolders = @(".env", ".venv", "venv", "ENV", "env.bak", "venv.bak")
foreach ($envFolder in $envFolders) {
    if (Test-Path $envFolder) {
        Remove-Item -Recurse -Force -Path $envFolder
    }
}

# Remove db.sqlite3 and db.sqlite3-journal
$filesToRemove = @("db.sqlite3", "db.sqlite3-journal")
foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item -Force -Path $file
    }
}

# Remove unit test/coverage reports
$testFolders = @("htmlcov", ".tox", ".nox", ".hypothesis", ".pytest_cache")
foreach ($testFolder in $testFolders) {
    if (Test-Path $testFolder) {
        Remove-Item -Recurse -Force -Path $testFolder
    }
}
Get-ChildItem -Recurse -Filter "*.coverage*" | ForEach-Object {
    Remove-Item -Force -Path $_.FullName
}
Get-ChildItem -Recurse -Filter "nosetests.xml" | ForEach-Object {
    Remove-Item -Force -Path $_.FullName
}
Get-ChildItem -Recurse -Filter "coverage.xml" | ForEach-Object {
    Remove-Item -Force -Path $_.FullName
}

# Remove other unnecessary files (pip-log.txt, pip-delete-this-directory.txt)
$otherFiles = @("pip-log.txt", "pip-delete-this-directory.txt")
foreach ($file in $otherFiles) {
    if (Test-Path $file) {
        Remove-Item -Force -Path $file
    }
}

# Stage the changes to remove the deleted files from Git
git rm -r --cached .
git add .

# Commit the changes
git commit -m "Remove ignored files and directories"
