(function($){
  var _xsrf = Tools.getCookie("_xsrf");

  // Comments Action Buttons
  $('.comment-content').hover(
    function(){
      $(this).find('.row-actions').show();
    },
    function(){
      $(this).find('.row-actions').hide();
    }
  );

  // Call reply Reveal
  $(document).on('click', '.reply', function(){
    var self = $(this),
        cid  = self.attr('cid'),
        did  = self.attr('did'),
        email = self.attr('email'),
        user = self.attr('user'),
        title = self.attr('title');

    if(email !== 'None'){
      if($('.admin-reply-area').length > 0) $('.admin-reply-area').remove();
      var target = self.parent().parent().parent();
      $('<tr class="admin-reply-area"></tr>').insertAfter(target);
      $('body').animate({ scrollTop: $('.admin-reply-area').offset().top - 200}, 900);
      var html = '<td class="content" colspan="4"><textarea></textarea><a class="tiny button secondary left" id="cel_reply_btn">取消</a><a class="tiny button success right" id="do_reply_btn" cid="' +
                  cid +
                  '" did="' +
                  did +
                  '" email="' +
                  email +
                  '" title="' +
                  title +
                  '" user="' +
                  user +
                 '">回复</a></td>';
      $('.admin-reply-area').hide().append(html).fadeIn(400);
    }else{
      alert('自己不能回复自己..')
    }
  });

  // Commit Comment Reply
  $(document).on('click', '#do_reply_btn', function(){
    var content = $(".admin-reply-area").find('textarea').val();
    var self = $(this),
        cid  = self.attr('cid'),
        did  = self.attr('did'),
        email = self.attr('email'),
        user = self.attr('user'),
        title = self.attr('title');

    Tools.reply(cid, did, email, title, content, user);

    $(".admin-reply-area").fadeOut(400, function(){
      var self = $(this);
      var copy = $('#comments_list_table tbody tr').first().clone();
      var first = copy.find('.role'),
          second = copy.find('.line-one'),
          third = copy.find('.diary-title a'),
          fourth = copy.find('.diary-time');

      first.text('博主回复');
      second.text(content);
      third.text(title);
      fourth.text(Tools.getTime());

      copy.insertAfter(self);
      self.remove();
    });
  });

  // Cancel Reply
  $(document).on('click', '#cel_reply_btn', function(){
    $(".admin-reply-area").fadeOut(400, function(){$(".admin-reply-area").remove()});
  });

  // Del Comment
  $(document).on('click', '.comment_del', function(){
    var self = $(this),
        cid = self.attr('cid'),
        did = self.attr('did');

    var url = '/admin/comment/del';

    $.ajax({
      type: 'POST',
      url: url,
      data: {did:did, cid:cid, _xsrf:_xsrf},
      success: function(){
        self.parents('tr').fadeOut();
      }
    });

  });

})(jQuery);
