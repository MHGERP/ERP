var AutoSave = function(textAreaDiv, ajax_func) {
    var t;
    var req;
    this.init = function() {
        $(document).on("keyup", textAreaDiv, function() {
            var content = $(this).html();
            var pid = $(this).attr("pid");
            t != null ? clearTimeout(t) : "";
            req != null ? req.abort() : "";
            t = setTimeout(function() {
                req = ajax_func(function() {req = null;}, {"content": content, "pid": pid, });
                t = null;
            }, 1000);
        });
    };
};

