function search_ajax_hint(msg) {
    return $("<div class=\"jumbotron my-4\" id=\"search-ajax-hint-jumbotron\"></div>").append($(msg));
}

function result_page_ajax(form) {
    var container = $("#search-ajax-info");
    if (!container.hasClass("search-ajax-onload")) {
        container.addClass("search-ajax-onload");
        $.get(
            "/ajax/result-page/",
            form,
            function (html, status) {
                var data = $(html);
                container.append(data).removeClass("search-ajax-onload");
                result_split_ajax(form);
                $(window).scroll(function () {
                    if ($(document).height() <= $(window).scrollTop() + $(window).height()) {
                        result_split_ajax(form);
                    }
                })
            }
        );
    }
}

function result_split_ajax(form) {
    var container = $("#search-ajax-container");
    if (!container.hasClass("search-ajax-onload")) {
        container.addClass("search-ajax-onload");
        var hint = $("#search-ajax-hint-jumbotron");
        hint.replaceWith(search_ajax_hint("<h4>Loading...</h4>"));
        $.get(
            "/ajax/result-split/",
            form,
            function (html, status) {
                var data = $(html);
                var hint = $("#search-ajax-hint-jumbotron");
                if (data.hasClass("search-ajax-has")) {
                    hint.replaceWith(search_ajax_hint("<h4>Scroll down to load more.</h4>"));
                    container.append(data).removeClass("search-ajax-onload");
                } else {
                    hint.replaceWith(data);
                    $(window).unbind("scroll");
                    container.removeClass("search-ajax-onload");
                }
            }
        );
    }
}
