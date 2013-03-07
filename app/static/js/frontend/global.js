(function($){

  // Comment Add Check
  $(document).on('click', '#comment_add_form_btn', function(){
    var self = $(this);
    var u_form = $('#comment_add_form'),
        u_name = u_form.find('.username'),
        u_email = u_form.find('.email'),
        u_comment = u_form.find('.comment');
    
      var flag1 = emptyCheck([u_name, u_email, u_comment]);
      var flag2 = emailCheck(u_email);

      if((flag1 == true) && (flag2 == true)){
        self.val('通知博主中...').fadeTo('slow', 0.5).attr('disabled', true);
        var _xsrf = getCookie("_xsrf");
        did = u_form.find('#did').val(),
        name = u_name.val(),
        email = u_email.val(),
        comment = u_comment.val();
        $.ajax({
          type: 'POST',
          url: '/comment/add',
          data: {username: name, did: did, email: email, comment: comment, _xsrf: _xsrf},
          success: function(data){
            self.val('提交').removeAttr('style').attr('disabled', false);
          },
          error: function(){
            self.val('发生错误, 错误信息已发送给博主');
          }
        });
        var time = getTime();
        var html = buildCommentHtml(name, time, comment);
        $('<li class="alt new-comment"></li>').appendTo('.commentlist');
        $('body').animate({ scrollTop: $('.new-comment:last-child').offset().top - 200}, 900);
        $('.new-comment:last-child').hide().append(html).fadeIn(4000);
        u_comment.val('');
      }
      else{
        return false;
      }
  });

  // auto img-position fix
  $(document).ready(function(){
    if($('p img').length > 0)
    $('p img').parent().css('text-align', 'center');
  });

  /*
  // gallary page funciton
  $(document).ready(function() {

    //blocksit define
    $(window).load(function() {
      $('#colum-container').BlocksIt({
        numOfCol: 5,
        offsetX: 8,
        offsetY: 8
      });
    });

    //window resize
    var currentWidth = 1200;
    $(window).resize(function() {
      var winWidth = $(window).width();
      var conWidth;
      if(winWidth < 660) {
        conWidth = 480;
        col = 2
      } else if(winWidth < 960) {
        conWidth = 720;
        col = 3
      } else if(winWidth < 1200) {
        conWidth = 960;
        col = 4;
      } else {
        conWidth = 1200;
        col = 5;
      }

      if(conWidth != currentWidth) {
        currentWidth = conWidth;
        $('#colum-container').width(conWidth);
        $('#colum-container').BlocksIt({
          numOfCol: col,
          offsetX: 8,
          offsetY: 8
        });
      }
    });
  }); 
  */
  // load code prettyprint
  $(document).ready(function(){
    if($('code').length>0){
      $('code').parent().addClass('prettyprint');
      prettyPrint();
    };
  });
  /*=======jQuery Functions===============*/
  
  // Get time
  function getTime(){
    var date = new Date();
    var year, month, day, hour, minute, second;
    hour = jsTimeFix(date.getHours());
    minute = jsTimeFix(date.getMinutes());
    second = jsTimeFix(date.getSeconds());
    year = date.getFullYear();
    month = jsTimeFix(date.getMonth()+1);
    day = jsTimeFix(date.getDate());
    var time = year + '-' + month + '-' + day + ' ' + hour +':' + minute + ':' + second;
    return time;
  };

  function jsTimeFix(time){
    if(time<10) return "0"+time;
    else return time;
  }

  // Comment HTML
  function buildCommentHtml(name, time, content){
    var html="";
    html += '<small class="commentmetadata"><a>' +
            time +
            '</a></small><cite>' +
            name + 
            '<span>:</span></cite><div class="comment-content"><p>' +
            content +
            '</p></div>';
    return html;
  };

  // Empty Check Function
  function emptyCheck(array){
    var flag = true;
    $.each(array, function(){
      var self = $(this);
      if(self.val().length == 0){
        self.addClass('error');
        flag = false;
        return;
      }else{
        self.removeClass('error');
        return true;
      }
    });
    return flag;
  };

  // Email Check Function
  function emailCheck(target){
    var rule = /^[a-zA-Z0-9]+[a-zA-Z0-9_.-]+[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+[a-zA-Z0-9_-]+.[a-z]{2,4}$/;
    if(!rule.test(target.val())){
      target.addClass('email-error');
      return false;
    }else{
      target.removeClass('email-error');
      return true;
    }
  };

  // Get Cookie Function 
  function getCookie(name) {
      var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
  };


})(jQuery);
