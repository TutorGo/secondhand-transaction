var dropdown = document.querySelectorAll('.sell_dropdown');
var dropdownArray = Array.prototype.slice.call(dropdown,0);
dropdownArray.forEach(function(el){
	var button = el.querySelector('a[data-toggle="sell_dropdown"]'),
			menu = el.querySelector('.sell_dropdown-menu'),
			arrow = button.querySelector('i.icon-arrow');
	$('.category-btn').click(function(){
		menu.classList.remove('show');
		menu.classList.add('hide');
		arrow.classList.remove('open');
		arrow.classList.add('close');
		event.preventDefault();
	});
	button.onclick = function(event) {
		if(!menu.hasClass('show')) {
			menu.classList.add('show');
			menu.classList.remove('hide');
			arrow.classList.add('open');
			arrow.classList.remove('close');
			event.preventDefault();
		}
		else {
			menu.classList.remove('show');
			menu.classList.add('hide');
			arrow.classList.remove('open');
			arrow.classList.add('close');
			event.preventDefault();
		}
	};
})

Element.prototype.hasClass = function(className) {
    return this.className && new RegExp("(^|\\s)" + className + "(\\s|$)").test(this.className);
};
