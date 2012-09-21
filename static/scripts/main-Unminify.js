//Main Page
$(document).ready(function (){
	beta = $('#text_box_beta').val();
	alpha = $('#text_box_alpha').val();
	if(beta==='' && alpha===''){
		drawWall(75,15);
	}else if(beta==undefined && alpha==undefined){
		drawWall(75,15);
	}else{
		drawWall(beta,alpha);
	}
});

function validate($obj, min, max){
	elem = $obj.val();
	var numericExpression = /^[.0-9]+$/;
	
  	if(elem.match(numericExpression)){
	  if(elem >= min && elem <= max){
		$obj.parent().next().text('OK');
	  }  
	}else{
		$obj.parent().next().css('color','red').text('ERROR');
	}
}

$('#text_box_beta').change(function (){
  $this = $(this);
  var beta = $this.val();
  var alpha = $('#text_box_alpha').val();
  drawWall(beta,alpha);
  validate($this,60,90);
});

$('#text_box_phi').change(function (){
  $this = $(this);
  validate($this,20,45);
});

$('#text_box_alpha').change(function (){
  $this = $(this);
  var beta = $('#text_box_beta').val();
  var alpha = $this.val();

  drawWall(beta,alpha);
  validate($this,0,25)
});

$('#text_box_delta').change(function (){
  $this = $(this);
  validate($this,0,30);
});

$('#text_box_ocr').change(function (){
  $this = $(this);
  validate($this,0,5);
});

//About Page
$(document).ready(function (){
	$('.equationList').on('click', '.list', function (){
		$(this).next().slideDown(200).siblings('dd').slideUp();
	});	
});