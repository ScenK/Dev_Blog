(function($){
  var _xsrf = Tools.getCookie("_xsrf");

  // post add and edit empty check
  $(document).bind('submit', '#add_post_form', function(){
    var self = $(this);
    var title = self.find('#post_title'),
        content = self.find('.xxlarge');
    var flag = Tools.emptyCheck([title, content]);

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
})(jQuery);
