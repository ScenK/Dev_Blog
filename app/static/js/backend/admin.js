(function($){
  var _xsrf = getCookie("_xsrf");
  /*------- start Post functions -------*/

  // post add and edit empty check
  $(document).on('submit', '#add_post_form', function(){
    var self = $(this);
    var title = self.find('#post_title'),
        content = self.find('.xxlarge');
    var flag = emptyCheck([title, content]);

    if(flag == true) self.submit();
    else return false;
  });

  // post edit auto remove ',' at last
  $(document).ready(function(){
    if($('.post_edit').length > 0){
      var str = $('input[name="tags"]').val().substr(0,$('input[name="tags"]').val().length-1);
      $('input[name="tags"]').val(str);
    }
  });
  /*------- end  Post functions -------*/

  /*------- start Comments functions -------*/

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

    reply(cid, did, email, title, content, user);

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
      fourth.text(getTime());

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

  /*--------- end Comments functions --------*/

  // Set Publish Date AJAX
  $(document).on('keydown', '.admin-diary-list .writeable', function(e){ 
    if(e.keyCode == 13){
      var self = $(this),
          did = self.attr('did'),
          date = self.text();
      var url = '/admin/diary/set-date';
      $.ajax({
        type: 'POST',
        url: url,
        data: {did:did, date:date, _xsrf:_xsrf},
        success: function(e){
          if(e === 'success'){
           alert('修改成功!');
           window.location.reload();
          }
        }
      });
    }
  });

  /*--------- start Diary Add Photo functions --------*/

  // Call Add Phtot Reveal
  $(document).on('click', '#add_photo', function(){ 
    $("#up_image").removeClass('success').addClass('normal').text('上传图片');
    $('#up_image_bak_url').val('');
    $("#add_photo_modal").reveal();
  });

  // Photo AJAX upload
  jQuery(function(){
    if($("#up_image").length>0){
      var fileType = "pic";
      new AjaxUpload('up_image', {
        multiple: true,
        action: '/admin/diary/add-photo',
        onSubmit : function(file, ext){
          if(fileType == "pic"){
            if(ext && /^(jpg|png|jpeg|gif)$/.test(ext)){
              $("#up_image").removeClass('normal').addClass('alert').text('上传中...');
              this.setData({
                _xsrf: _xsrf
              });
            }else {
              alert('文件格式不正确');
              return;
            }
          }
        },
        onComplete: function(file, response){
          $("#up_image").removeClass('alert').addClass('success').text('Markdown代码:');
          $('#up_image_bak_url').val(response);
        }
      });
    }
  });

  /*--------- end Diary Add Photo functions --------*/

  /*--------- start Gallary functions --------*/

  // call add gallary reveal
  $(document).on('click', '#call_add_gallary_modal', function(){ 
    var modal = $("#gallary_add_modal");
    modal.find('input, textarea').val('');
    modal.reveal();
  });

  // Do add gallary submit
  $(document).on('click', '#do_add_gallary', function(){ 
    var modal = $("#gallary_add_modal"),
        title = modal.find('input').val(),
        desc  = modal.find('textarea').val(); 

    var url = '/admin/gallary/add';
    $.ajax({
      type: 'POST',
      url: url,
      data:{title:title, desc:desc, _xsrf:_xsrf},
      success: function(e){
        window.location.reload();
      }
    });
  });

  // call add photos reveal
  $(document).on('click', '#call_add_photos_modal', function(){ 
    var modal = $("#add_photos_modal");
    modal.reveal();
  });

  // call add photos use fineuploader
  $(document).ready(function() {
    var errorHandler = function(event, id, fileName, reason) {
      qq.log("id: " + id + ", fileName: " + fileName + ", reason: " + reason);
    };
    var fileNum = 0;
    var gid = $('#do_add_photos').attr('gid');

    $('#add_photos_area').fineUploader({
      autoUpload: false,
      uploadButtonText: "Select Files",
      request: {
        endpoint: "/admin/gallary/add-photo"
      }
    }).on('submit', function(event, id, filename){
      $(this).fineUploader('setParams', {'_xsrf': _xsrf, 'gid': gid});
    }).on('complete', function(event, id, filename, responseJSON){
    }).on('error', errorHandler);

    $('#do_add_photos').click(function() {
      $('#add_photos_area').fineUploader("uploadStoredFiles");
    });

  });

  /*--------- end Gallary functions --------*/

  /*--------- start Category functions --------*/

  // cal new category modal
  $(document).on('change', '#categories_select', function(){ 
    var self = $(this);
    if(self.val() === '创建新分类'){
      $("#add_category_input").val('');
      var modal = $("#add_category_modal");
      modal.reveal();
    }else{
      var cid = self.find(':selected').attr('cid');
      $("#category_id").val(cid);
    }
  });
  
  // do add new category
  $(document).on('click', '#do_add_category', function(){ 
    var cat = $("#add_category_input").val(),
        url = '/admin/category/add';
    $.ajax({
      type: 'POST',
      url: url,
      data: {category:cat, _xsrf:_xsrf},
      success: function(data){
        var obj = $.parseJSON(data);
        if(obj.success === 'true'){
          $("#category_id").val(obj.cid);
          $('#categories_select :selected').text(cat);
          $('#categories_select').append('<option>创建新分类</option>');
          $("#add_category_modal").trigger('reveal:close');
        }else{
          alert('数据库返回错误');
        }
      }
    });
  });
  /*--------- end Category functions --------*/
  
  /*------=========== jQuery Functions ==========-----*/

  // Empty Check 
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
  };

  // AJAX Comment Reply Function
  function reply(cid, did, email, title, content, user) {
      var url = '/admin/comment/reply';
      $.ajax({
        type: 'POST',
        url: url,
        data: {content:content, did:did, cid:cid, _xsrf:_xsrf, email:email, title:title, user:user}
      });
  };

  // AJAX Get Cookie Function
  function getCookie(name) {
      var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
  };

  /*------=========== end jQuery functions ==========-----*/

})(jQuery);
