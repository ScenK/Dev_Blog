var Tools = {

  emptyCheck: function (array) {
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
  },

  getTime: function () {
    var date = new Date();
    var year, month, day, hour, minute, second;
    hour = this.jsTimeFix(date.getHours());
    minute = this.jsTimeFix(date.getMinutes());
    second = this.jsTimeFix(date.getSeconds());
    year = date.getFullYear();
    month = this.jsTimeFix(date.getMonth()+1);
    day = this.jsTimeFix(date.getDate());
    var time = year + '-' + month + '-' + day + ' ' + hour +':' + minute + ':' + second;
    return time;

  },

  jsTimeFix: function (time) {
    return time<10 ? "0"+time : time;
  },

  reply: function (cid, did, email, title, content, user) {
    var url = '/admin/comment/reply';
    $.ajax({
      type: 'POST',
      url: url,
      data: {content:content, did:did, cid:cid, _xsrf:this.getCookie('_xsrf'), email:email, title:title, user:user}
    });
  },

  getCookie: function (name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
  }

}
