window.MathJax = {
    AuthorInit: function () {
        MathJax.Hub.Register.StartupHook("End", function () {
            window.status = "Rendered"
        });
    }
};