function sendFile(file, editor, welEditable) {
    data = new FormData();
    data.append("file", file);
    $.ajax({
        data: data,
        type: "POST",
        url: "/dashboard/upload_img/",
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            var url = data.src;
            editor.insertImage(welEditable, url);
        }
    });
}
