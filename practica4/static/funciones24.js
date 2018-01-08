$(document).ready(function(){
// Reiniciar el tamaño de la fuente
var tamOriginal = $('a').css('font-size');
$(".reiFuente").click(function(){
        $('a').css('font-size', tamOriginal);
});
// Incrementar el tamaño de la fuente
$(".aumFuente").click(function(){
        var tamActual = $('a').css('font-size');
        var tamActualNum = parseFloat(tamActual, 10);
        var nuevaFuente = tamActualNum*1.2;
        $('a').css('font-size', nuevaFuente);
       
});
// Incrementar el tamaño de la fuente
$(".disFuente").click(function(){
        var tamActual = $('a').css('font-size');
        var tamActualNum = parseFloat(tamActual, 10);
        var nuevaFuente = tamActualNum*0.8;
        $('a').css('font-size', nuevaFuente);

});


$("button").click(function(){
        
        $('div#cuerpo2').css('background-color', 'red');
       
       
    });

});
