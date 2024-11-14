#!/bin/bash

# Update package list
sudo apt update

# Install OCRmyPDF and Tesseract OCR
echo "Installing OCRmyPDF and Tesseract OCR..."
sudo apt install -y tesseract-ocr
sudo apt-get install -y tesseract-ocr-chi-tra
sudo apt install -y ocrmypdf
apt-cache search tesseract-ocr

# Install JBIG2 encoder dependencies for OCRmyPDF
echo "Installing JBIG2 encoder dependencies..."
sudo apt install -y autotools-dev automake libtool libleptonica-dev

# Clone JBIG2 encoder repository and build it
echo "Cloning and building JBIG2 encoder..."
git clone https://github.com/agl/jbig2enc
sleep 5
cd jbig2enc
./autogen.sh
./configure && make
sudo make install
cd ..

# Install additional development tools and libraries
echo "Installing additional libraries and tools..."
sudo apt install -y build-essential libpoppler-cpp-dev pkg-config python3-dev

# Install Python package pdftotext
echo "Installing Python package: pdftotext..."
pip install pdftotext

echo "Installation complete."

