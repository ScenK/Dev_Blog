(function($){
  var _xsrf = Tools.getCookie("_xsrf");

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

})(jQuery);
