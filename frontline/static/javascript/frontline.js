(function($) {
    $(function() {
        new Frontline();
    });

    var Frontline = function() {
        this.initDom();
        this.initActions();
    };

    Frontline.prototype = {
        initDom: function() {
            this.$panel = $('#frontline-panel');
            
            this.inline_edit = $('.frontline-edit.inline');
            this.inline_edit_content = this.inline_edit.find('.frontline-content');
            this.inline_edit_btn = this.inline_edit.find('.frontline-edit-btn');
            this.richtext_edit = $('.frontline-edit.lightbox');
            this.image_edit = $('.frontline-image-edit');

            this.open_panel_btn = this.$panel.find('.frontline-open-panel-btn');

            this.active_anchor = null;

            this.save_btn = $('#live-edit-save');

            this.lightbox_container = $('#frontline-lightbox');

            this.edit_start_btn = $('#live-edit-start');
            this.edit_stop_btn = $('#live-edit-stop');
            this.edit_save_btn = $('#live-edit-save');

            this.updated_warning = $('#updated-warning');
        },
        // init user actions
        initActions: function() {
            this.edit_start_btn.click($.proxy(this.startEditing, this));
            this.edit_stop_btn.click($.proxy(this.stopEditing, this));
            this.edit_save_btn.click($.proxy(this.saveAll, this));

            this.selectedContent = null;
            var self = this;

            // focusin inline edit
            this.inline_edit.focusin(function() {
                var $this = $(this);
                var $button = $this.find('.frontline-edit-btn');
                var $content = $this.find('.frontline-content');
                $button.addClass('edit');

                self.selectedContent = $(this).html();
            }).focusout(function() {
                // var $this = $(this);
                // // selected content stayed the same, do not save
                // if(self.selectedContent == $this.html())
                //     return;

                // // if its not richtext, then call striptags
                // if(!$this.hasClass('tinymce'))
                //     $this.html(self.stripTag($this.html()));

                // // save data
                // self.saveData();

                // self.selectedContent = null;
            });

            // click on edit button
            this.inline_edit_btn.click(function(event) {
                event.preventDefault();
                var $this = $(this);
                var $content = $(this).parent().find('.frontline-content');
                if(!$this.hasClass('edit')) {
                    $this.addClass('edit');
                    $content.focus();
                }
                else {
                    $(window).focus();
                    $this.removeClass('edit');
                    self.saveData($this.parent());
                }
            });

            this.open_panel_btn.click(function(event) {
                event.preventDefault();
                var $this = $(this);
                if(!self.is_out) {
                    if(!self.panel_height)
                        self.panel_height = self.$panel.find('.frontline-inner').outerHeight();
                    self.$panel.height(self.panel_height).css('right', 0).addClass('out');
                    self.is_out = true;
                }
                else {
                    self.$panel.height(60).css('right', -110).removeClass('out');
                    self.is_out = false;
                }
            });
        },
        startEditing: function() {
            this.inline_edit.addClass('frontline-marked-editable');
            this.inline_edit_content.attr('contenteditable', 'true');
            this.richtext_edit.addClass('frontline-marked-editable');
            this.image_edit.addClass('frontline-marked-editable');


            this.edit_stop_btn.show();
            this.edit_start_btn.hide();

            tinymce.init(window.tinymce_inline_config);

            var self = this;

            // open richtext editor
            this.richtext_edit.click(function(event) {
                event.preventDefault();
                self.current_edit = $(this);
                self.current_content = self.current_edit.find('.frontline-content');
                self.active_name = self.current_edit.attr('data-name');
                self.openRichtextInLightbox(self.active_name);
            });

            // open image upload form
            this.image_edit.click(function(event) {
                event.preventDefault();
                self.current_edit = $(this);
                self.current_content = self.current_edit.find('.frontline-content');
                self.active_name = self.current_edit.attr('data-name');
                self.openImageFormInLightbox(self.active_name);
            });
        },
        stopEditing: function() {
            this.inline_edit.attr('contenteditable', 'false').removeClass('frontline-marked-editable');
            this.richtext_edit.removeClass('frontline-marked-editable');
            this.image_edit.removeClass('frontline-marked-editable');

            this.edit_stop_btn.hide();
            this.edit_start_btn.show();

            tinymce.remove('span.tinymce.inline');

            this.richtext_edit.unbind();
            this.image_edit.unbind();
        },
        // save inline data
        saveData: function() {
            var inline_text_list = '';
            this.inline_edit.each($.proxy(function(key, value) {
                var $value = $(value);
                var stripped_tring = $value.html();
                if(!$value.hasClass('tinymce'))
                    stripped_tring = this.stripTag($value.html());
                inline_text_list += $value.attr('data-name') + "=" + escape(stripped_tring) + '&';
            }, this));

            $.ajax({
                url: '/api/save/',
                method: 'POST',
                data: inline_text_list
            });
            this.showSaveView();
        },
        // display small window to show that data is saving
        showSaveView: function() {
            if(!this.save_progress_view)
                this.save_progress_view = $('#frontline-save-progress');
            
            this.save_progress_view.fadeIn();
            setTimeout($.proxy(function() {
                this.save_progress_view.fadeOut();
            }, this), 1500);
        },
        showUpdatedWarning: function() {
            this.updated_warning.show();
        },
        stripTag: function(text) {
            return text.replace(/(?!<br>)(<([^>]+)>)/ig,"");
        },
        openRichtextInLightbox: function(name) {
            var self = this;
            $.ajax({
                url: '/api/richtext-form/' + name + '/',
                success: function(result) {
                    self.lightbox_container.find('.content').html(result);
                    // lightbox save
                    self.lightbox_container.find('.save').click(function(event) {
                        event.preventDefault();
                        var data = $('#frontline-richtext-form').serialize();
                        data += '&data=' + tinymce.activeEditor.getContent();
                        $.post('/api/richtext-form/' + name + '/', data,
                            function(result) {
                                self.current_content.html(result);
                            });
                        self.cancelLightBox();
                    });
                    // lightbox close
                    self.lightbox_container.find('.cancel').click(function(event) {
                        event.preventDefault();
                        self.cancelLightBox();
                    });
                }
            });

            this.lightbox_container.show();
            this.tinymce = tinymce.init(window.tinymce_config);
            tinymce.activeEditor.setContent($('[data-name="' + this.active_name + '"]').html());
        },
        openImageFormInLightbox: function(name) {
            var self = this;
            $.ajax({
                url: '/api/image-upload-form/' + name,
                success: function(result) {
                    self.lightbox_container.find('.content').html(result);

                    // lightbox close
                    self.lightbox_container.find('.cancel').click(function(event) {
                        event.preventDefault();
                        self.cancelLightBox();
                    });

                    self.lightbox_container.find('#frontline-image-upload-form').submit(function(event) {
                        event.preventDefault();
                        var form_data = new FormData(this);
                        $.ajax({
                            type:'POST',
                            url: '/api/image-upload-form/' + name + '/?option=' +
                                self.current_edit.attr('data-option'),
                            data: form_data,
                            cache: false,
                            contentType: false,
                            processData: false,
                            success:function(result){
                                self.lightbox_container.find('.content').html(result);
                                // location.reload();
                            },
                            error: function(result){
                                self.lightbox_container.find('.content').html(result);
                            }
                        });
                    });
                }
            });
            this.lightbox_container.show();
        },
        cancelLightBox: function() {
            this.lightbox_container.hide();
        },
        saveAll: function() {
            var self = this;
            this.inline_edit_btn.removeClass('edit');
            this.inline_edit.each(function(key, value) {
                self.saveData($(value));
            });
        }
    };

    function getCookie(name) {
        var cookieValue = null;
        if(document.cookie && document.cookie) {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})($);