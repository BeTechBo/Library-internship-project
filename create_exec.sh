if [ -f main.exe ]; then
    rm main.exe
fi

pyinstaller --onefile  --noconsole RecognitionApplication/main.py

if [ $? -eq 0 ]; then
    mv dist/main.exe .

    rm -rf dist build main.spec

    echo "Build successful."
else
    echo "Build failed. Check the PyInstaller output for details."
    exit 1
fi