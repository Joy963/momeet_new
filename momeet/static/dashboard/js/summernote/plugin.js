(function (factory) {
    /* global define */
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['jquery'], factory);
    } else {
        // Browser globals: jQuery
        factory(window.jQuery);
    }
}(function ($) {
    // template, editor
    var tmpl = $.summernote.renderer.getTemplate();
    clear_p = function () {

        /* 仅限于编辑器内的p标签 */

        $(".note-editable p").each(function () {

            /* 获取p标签下的子元素个数 */

            var childen_e_count = $(this).children().length;

            /*如果p里面没有子元素，并且p里是空的*/

            if (childen_e_count === 0) {
                if ($(this).text().trim() === "") {
                    $(this).remove();
                }
            }

            var i = 0;

            i += $(this).find("img").length;

            /*如果 p 里没有 img */

            if (i === 0) {
                /*如果p里包含br*/
                if ($(this).find("br").length > 0) {
                    /*如果p里没有内容*/
                    if ($(this).text().trim() === "") {
                        $(this).remove();
                    }
                }
            }
        });
    };

    reset_p = function (event, editor, layoutInfo, p_class) {
        var $editable = layoutInfo.editable();
        var info = editor.getLinkInfo($editable);
        var text = info.text;
        if (text === '' || text === undefined) {
            return;
        } else {
            var select_element = info.range.ec.parentElement;
            console.log(select_element);
            var node= $("<p class='"+p_class+"'>" + text + "</p>");
            editor.insertNode($editable, node[0]);
            clear_p();
            
        }
    };

    // add plugin
    $.summernote.addPlugin({
        name: 'momeet_plugin', // name of plugin
        buttons: { // buttons
            titledesc: function () {
                return tmpl.iconButton('fa fa-bold', {
                    title: '设为标题',
                    event: 'titledesc',
                    hide: true
                });
            },
            clear_titledesc: function () {
                return tmpl.iconButton('fa fa-eraser', {
                    title: '取消标题',
                    event: 'clear_titledesc',
                    hide: true
                });
            }
        },

        events: { // events
            titledesc: function (event, editor, layoutInfo) {
                reset_p(event, editor, layoutInfo, 'titledesc');
            },
            clear_titledesc: function (event, editor, layoutInfo) {
                reset_p(event, editor, layoutInfo, '');
            }
        }
    });
}));
