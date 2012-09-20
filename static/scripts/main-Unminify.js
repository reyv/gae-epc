//Main Page
function startWall(Beta,Alpha){
  if(Beta===0 && Alpha===0){
    drawWall(75,15);
  }else{
    drawWall(Beta,Alpha);
  }
}

$(document).ready(startWall(
  $('#text_box_beta').val(),$('#text_box_alpha').val()
));

function validate(elem, id, min, max){
	var numericExpression = /^[.0-9]+$/;
	
  	if(elem.match(numericExpression)){
	  if(elem >= min && elem <= max){
	    $(id).css("color","#3bd2e3");
	    $(id).html("OK"); 
	  }  
	}else{
	    $(id).css("color",red);
	    $(id).html("ERROR");
	}    
}

$('#text_box_beta').change(function (){
  var beta = $(this).val();
  var alpha = $('#text_box_alpha').val();
  
  drawWall(beta,alpha);
  validate(beta,'#verify_beta',60,90)
});

$('#text_box_phi').change(function (){
  var value = $(this).val();
  validate(value,'#verify_phi',20,45);
});

$('#text_box_alpha').change(function (){
  var beta = $('#text_box_beta').val();
  var alpha = $(this).val();

  drawWall(beta,alpha);
  validate(alpha,'#verify_alpha',0,25)
});

$('#text_box_delta').change(function (){
  var value = $(this).val();
  validate(value,'#verify_delta',0,30);
});

$('#text_box_ocr').change(function (){
  var value = $(this).val();
  validate(value,'#verify_ocr',0,5);
});

//About Page
$(document).ready(function (){
	$('.equationList').on('click', '.list', function (){
		$(this).next().slideDown(200).siblings('dd').slideUp();
	});	
});