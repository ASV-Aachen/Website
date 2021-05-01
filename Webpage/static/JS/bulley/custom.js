// Empty JS for your own code to be here


function clickDropdown() {
    if ($('.navbar-toggler').css("display") === "none") {
        $('.dropdown-toggle').click(function () {
            window.location.href = $(this).attr('href');
            return false;
        });
    }
}
$(document).ready(function () {
    clickDropdown();
    $(window).resize(function () {
        clickDropdown();
    });
});

$(document).ready(function(){
	$(window).scroll(function () {
			if ($(this).scrollTop() > 50) {
				$('#back-to-top').fadeIn();
			} else {
				$('#back-to-top').fadeOut();
			}
		});
		// scroll body to 0px on click
		$('#back-to-top').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 400);
			return false;
		});
});