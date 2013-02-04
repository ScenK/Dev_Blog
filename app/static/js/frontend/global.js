(function($){

  // Profile Slide
  $('.avatar').live('click', function(){
    $('.profile').slideToggle('fast');
  });

  // AJAX Load More 
  $('.load-more').live('click', function(){
    var self   = $(this),
        offset = parseInt(self.attr('offset'));
    if(self.text() !== '没有更多文章了...')
      loadMore(self, offset);
  });

  // Comment Add Check
  $('#comment_add_form_btn').live('click', function(){
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
        $('<div class="single-diary comments new-comment"></div>').appendTo('.comments-area');
        $('body').animate({ scrollTop: $('.new-comment:last-child').offset().top - 200}, 900);
        $('.new-comment:last-child').hide().append(html).fadeIn(4000);
        u_comment.val('');
      }
      else{
        return false;
      }
  });

  // Call Search
  $('#call_search').live('click', function(){
    $('#___gcse_0').fadeIn().addClass('gsc-results-wrapper-visible');
    $('#cloudy').addClass('gsc-modal-background-image-visible');
  });

  // Cancel Search
  $('.gsc-results-close-btn, .gsc-modal-background-image, #cloudy').live('click', function(){
    $('#cloudy').removeClass('gsc-modal-background-image-visible');
    $('gsc-modal-background-image').removeClass('gsc-modal-background-image-visible'); 
    $('#___gcse_0').fadeOut().removeClass('gsc-results-wrapper-visible');
  });

  // Comment testarea auto height
  $('#comment_add_form textarea').live('keydown', function(e){
    var self = $(this);
    if(e.keyCode == 13){
      self.height(self.height()+15);
    };
  });

  // auto img-position fix
  $(document).ready(function(){
    if($('p img').length > 0)
      $('p img').parent().css('text-align', 'center');
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
    html += '<div class="content"><div class="line-one"><b>' +
            name +
            '</b><span>' +
            time + 
            '</span></div><div class="line-two">' +
            content +
            '</div></div>';
    return html;
  };

  // Path Function
  $(function(){
    var delay = 40, delayTime, btns = $('.btn');
    $('#base-button').toggle(function(){
      $(this).addClass('open');
      btns.each(function(i){
        delayTime = i * delay;
        var ele = $(this);
        window.setTimeout(function(){
          ele.addClass('open');
        }, delayTime);
      });
    }, function(){
      $(this).removeClass('open');
      var ii = 0;
      $($(btns).get().reverse()).each(function(i){
        delayTime = i * delay;
        var ele = $(this);
        window.setTimeout(function(){
          ele.removeClass('open');
        }, delayTime);
      });
    });
  });

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


  // Ajax Load More Function
  function loadMore(self, offset){

    var url = '/diary/load';

    $.getJSON(url, {offset: offset}, function(e){
      if(e.length != 0){
        $.each(e, function(i, v){
          var new_diary = $('.single-diary').first().clone()
                                    .appendTo('.home');
          var obj = $.parseJSON(v);
          new_diary.find('.diary-title').empty().html(obj.title).attr({'href': '/diary/detail/'+obj._id, 'title': obj.title});
          new_diary.find('.summary').empty().html(obj.summary);
          new_diary.find('.publish-time').empty().html(obj.publish_time);
        });
        offset += 3;
        self.remove().appendTo('.home').attr('offset', offset);
      }
      else{
        self.text('没有更多文章了...');
      }
    });
  }; 

  // AJAX Get Cookie Function 
  function getCookie(name) {
      var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
  };

})(jQuery);
