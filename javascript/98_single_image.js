// Single Image Tagger - Clipboard copy function
function copyTagsToClipboard() {
    const textarea = document.querySelector('#single_image_tags textarea');
    if (textarea && textarea.value) {
        navigator.clipboard.writeText(textarea.value).then(function() {
            // success
        }).catch(function() {
            // fallback
            textarea.select();
            document.execCommand('copy');
        });
        return [textarea.value, "コピーしました"];
    }
    return ["", "コピー対象がありません"];
}

// Single Image Tagger - Drag and Drop override
(function() {
    function getPreviewArea() {
        return document.getElementById('single_image_preview');
    }

    // ブラウザがファイルを開くデフォルト挙動を window レベルで阻止（画像がある時のみ）
    window.addEventListener('dragover', (e) => {
        const preview = getPreviewArea();
        if (preview && (preview === e.target || preview.contains(e.target))) {
            // 画像が存在するか（＝imgタグがあるか）確認
            const hasImage = preview.querySelector('img') !== null;

            if (hasImage) {
                // 画像がある場合のみ、ブラウザやGradioの挙動を止めて独自処理の準備をする
                e.preventDefault();
                e.stopPropagation();
                e.dataTransfer.dropEffect = 'copy';
            }
            // 画像がない（空）の場合は、Gradio 本来のドロップ受け入れ機能に任せる
        }
    }, true);


    window.addEventListener('drop', (e) => {
        const preview = getPreviewArea();
        if (preview && (preview === e.target || preview.contains(e.target))) {
            const files = e.dataTransfer.files;
            if (files && files.length > 0 && files[0].type.startsWith('image/')) {
                
                // 実際に画像が表示されているか img タグで確認
                const hasImage = preview.querySelector('img') !== null;

                if (hasImage) {
                    // 画像がある場合のみ介入
                    
                    // クリアボタンを探す
                    let clearButton = preview.querySelector('button[aria-label="Clear"], .clear-button');
                    if (!clearButton) {
                        const buttons = preview.querySelectorAll('button');
                        for (const btn of buttons) {
                            // クリアボタンは通常 svg を含み、テキストがほぼ空
                            if (btn.innerHTML.includes('svg') && btn.innerText.trim().length < 5) {
                                if (btn.offsetParent !== null) {
                                    clearButton = btn;
                                    break;
                                }
                            }
                        }
                    }

                    if (clearButton) {
                        e.preventDefault();
                        e.stopPropagation();
                        clearButton.click();
                        
                        let attempts = 0;
                        const injectFile = () => {
                            const input = preview.querySelector('input[type="file"]');
                            if (input) {
                                const dataTransfer = new DataTransfer();
                                dataTransfer.items.add(files[0]);
                                input.files = dataTransfer.files;
                                input.dispatchEvent(new Event('change', { bubbles: true }));
                            } else if (attempts < 20) {
                                attempts++;
                                setTimeout(injectFile, 50);
                            }
                        };
                        setTimeout(injectFile, 100);
                    }
                }
                // 画像がない（空）の場合は何もしないことで Gradio 本来のドロップが機能する
            }
        }
    }, true);
})();
