var slider = document.getElementById('slider');
var slide = document.getElementById('slide');
var line1 = document.getElementById('line1');
var line2 = document.getElementById('line2');
var line3 = document.getElementById('line3');
var line4 = document.getElementById('line4');

line1.onclick = function(){
    slider.style.transform = 'translateX(0)'
    slide.style.top = '0px'
}
line2.onclick = function(){
    slider.style.transform = 'translateX(-25%)'
    slide.style.top = '80px'
}
line3.onclick = function(){
    slider.style.transform = 'translateX(-50%)'
    slide.style.top = '160px'
}
line4.onclick = function(){
    slider.style.transform = 'translateX(-75%)'
    slide.style.top = '240px'
}
