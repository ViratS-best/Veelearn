/**
 * Veelearn Image Optimization Utility
 * Compress on upload, WebP format, lazy load, responsive sizes
 */

class ImageOptimizer {
    constructor() {
        this.maxFileSize = 5 * 1024 * 1024; // 5MB
        this.maxWidth = 1920;
        this.maxHeight = 1080;
        this.quality = 0.8;
        this.init();
    }

    init() {
        this.setupImageUploadListeners();
        this.setupResponsiveImages();
        console.log('Image optimizer initialized');
    }

    setupImageUploadListeners() {
        const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', this.handleImageUpload.bind(this));
        });
    }

    async handleImageUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            return;
        }

        if (file.size > this.maxFileSize) {
            alert(`File size exceeds ${this.maxFileSize / 1024 / 1024}MB limit`);
            return;
        }

        try {
            const optimizedImage = await this.optimizeImage(file);
            this.replaceFileInput(event.target, optimizedImage);
        } catch (error) {
            console.error('Image optimization error:', error);
        }
    }

    async optimizeImage(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    let width = img.width;
                    let height = img.height;

                    // Calculate dimensions while maintaining aspect ratio
                    if (width > this.maxWidth) {
                        height = (height * this.maxWidth) / width;
                        width = this.maxWidth;
                    }

                    if (height > this.maxHeight) {
                        width = (width * this.maxHeight) / height;
                        height = this.maxHeight;
                    }

                    canvas.width = width;
                    canvas.height = height;

                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, width, height);

                    // Convert to WebP if supported
                    const mimeType = this.supportsWebP() ? 'image/webp' : file.type;
                    
                    canvas.toBlob((blob) => {
                        const optimizedFile = new File([blob], file.name.replace(/\.[^.]+$/, '.webp'), {
                            type: mimeType,
                            lastModified: Date.now()
                        });
                        resolve(optimizedFile);
                    }, mimeType, this.quality);
                };
                img.onerror = reject;
                img.src = e.target.result;
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    supportsWebP() {
        const canvas = document.createElement('canvas');
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    }

    replaceFileInput(input, optimizedFile) {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(optimizedFile);
        input.files = dataTransfer.files;
    }

    setupResponsiveImages() {
        // Add srcset to images for responsive loading
        const images = document.querySelectorAll('img:not([srcset])');
        images.forEach(img => {
            if (img.src) {
                this.addSrcSet(img);
            }
        });
    }

    addSrcSet(img) {
        const src = img.src;
        const extension = src.split('.').pop();
        
        // Generate srcset with different sizes
        const sizes = [320, 640, 960, 1280];
        const srcset = sizes.map(size => {
            return `${src}?w=${size} ${size}w`;
        }).join(', ');
        
        img.srcset = srcset;
        img.sizes = '(max-width: 600px) 320px, (max-width: 900px) 640px, 960px';
    }

    async compressImage(file, quality = this.quality) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;

                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);

                    canvas.toBlob((blob) => {
                        const compressedFile = new File([blob], file.name, {
                            type: file.type,
                            lastModified: Date.now()
                        });
                        resolve(compressedFile);
                    }, file.type, quality);
                };
                img.onerror = reject;
                img.src = e.target.result;
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    async convertToWebP(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;

                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);

                    canvas.toBlob((blob) => {
                        const webpFile = new File([blob], file.name.replace(/\.[^.]+$/, '.webp'), {
                            type: 'image/webp',
                            lastModified: Date.now()
                        });
                        resolve(webpFile);
                    }, 'image/webp', this.quality);
                };
                img.onerror = reject;
                img.src = e.target.result;
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    getImageInfo(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const img = new Image();
                img.onload = () => {
                    resolve({
                        width: img.width,
                        height: img.height,
                        aspectRatio: img.width / img.height,
                        size: file.size,
                        type: file.type
                    });
                };
                img.onerror = reject;
                img.src = e.target.result;
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }
}

// Initialize global image optimizer
window.imageOptimizer = new ImageOptimizer();

console.log('Image optimization utility loaded');
