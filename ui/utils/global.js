var body = $("body");
var sm = $('#search-modal'),
    ee = $('#search-modal form, .exit');

function closeSearchBox() {
    sm.removeClass('appear');
    ee.removeClass('pop');
    body.removeClass('modal-open');
    return false;
}

function initMasonry() {
   /* var blog = $('.blog');
    if (blog.length > 0) {
        blog.masonry({
            itemSelector: '.blog-item',
            transitionDuration: '0',
            resize: false,
            columnWidth: '.blog-sizer',
            percentPosition: true
        });
    }*/
}