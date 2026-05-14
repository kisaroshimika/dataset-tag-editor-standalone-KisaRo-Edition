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
