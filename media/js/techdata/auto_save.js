var AutoSave = function(textAreaDiv, save_func, timeout) {
    /*
     * Author: JunHU
     * Description: binding the editable div element, auto save the content to save_func timeout sec after "keyup" event
     * args: textAreaDiv: selector name; save_func: save function support callback; timeout: timeout variable
     */
    var t;
    var req;
    this.init = function() {
        $(document).on("keyup", textAreaDiv, function() {
            var thisElement = $(this);
            t != null ? clearTimeout(t) : "";
            req != null ? req.abort() : "";
            t = setTimeout(function() {
                req = save_func(function() {req = null;}, thisElement);
                t = null;
            }, timeout);
        });
    };
};
