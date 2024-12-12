document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        // 处理上传的图片
        console.log('文件已选择:', file.name);
    }
}); 