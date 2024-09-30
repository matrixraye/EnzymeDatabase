/*
***********周玉琦**********
*********20240215*********
*/
$(".Indnava").click(function(){
    if(!$(this).hasClass('on')){
        $(this).next(".IndnavF").slideDown(400);
        $(this).addClass("on");
    }else{
        $(this).next(".IndnavF").slideUp(400);
        $(this).removeClass("on");
    }
});



//$('.IndCon').css('padding-top', parseFloat($('header').height()));
//导航下拉
$(".MenuA").mouseover(function(){
    if(parseFloat($('body').width())>960){
        $(this).next(".MenuF").slideDown(400);
        $(this).addClass("menuO");
    }
  });
$(".Menu ul li").mouseleave(function(){
    if(parseFloat($('body').width())>960){
        $(this).children(".MenuF").slideUp(400);
        $(this).children(".MenuA").removeClass("menuO");
        $(".MenuZ").slideUp(400);
    }
});
//wap下拉菜单
$('.hd_nav').click(function(){	  
  if(!$(this).hasClass('active')){
    $(this).addClass('active');
    $('.Menu').fadeIn(200);
  }else{
    $(this).removeClass('active');
    $('.Menu').fadeOut(100);
  }
});
$(".MenuA").click(function(){
    if(parseFloat($('body').width())<960){
        if(!$(this).hasClass('menuO')){
            $(".MenuF").slideUp(400);
            $(".MenuA").removeClass("menuO");
            $(this).next(".MenuF").slideDown(400);
            $(this).addClass("menuO");
        }else{
            $(this).next(".MenuF").slideUp(400);
            $(this).removeClass("menuO");
        }
    }
});

$(".minus").click(function () {
  if ($(this).next().val() > 0) {
    $(this)
      .next()
      .val(parseFloat($(this).next().val()) - 1);
  }
});
$(".plus").click(function () {
  $(this)
    .prev()
    .val(parseFloat($(this).prev().val()) + 1);
});



$(window).resize(function () {          //当浏览器大小变化时
    if($(window).width()>959){$('.Menu').css("display","block");$('.hd_nav').addClass('active');
	  }else{$('.Menu').css("display","none");$('.hd_nav').removeClass('active');}
});	

















