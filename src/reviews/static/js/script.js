document.addEventListener('DOMContentLoaded', function () {
  const ratingButtons = document.querySelectorAll('.star-btn');
  const hiddenInput = document.querySelector('input[name="rating"]');

  for (let i = 0; i < ratingButtons.length; i++) {
    ratingButtons[i].addEventListener('click', function () {
      const rating = this.getAttribute('data-rating');
      hiddenInput.value = rating;

      for (let j = 0; j < ratingButtons.length; j++) {
        if (j < rating) {
          ratingButtons[j].classList.add('selected');
        } else {
          ratingButtons[j].classList.remove('selected');
        }
      }
    });
  }
});

$(document).ready(function() {
    $("#username-field").autocomplete({
        source: "/search_user/",
        minLength: 2,
        select: function(event, ui) {
            $("#search_user").val(ui.item.value);
        }
    });
});
