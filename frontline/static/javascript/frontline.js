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

            this.richtext_edit = $('.frontline-edit.lightbox');

            this.active_anchor = null;

            this.save_btn = $('#live-edit-save');

            this.lightbox_container = $('#frontline-lightbox');

            this.contenttypes_edit_btns = $('.live-edit-contenttype-edit');

            this.edit_start_btn = $('#live-edit-start');
            this.edit_stop_btn = $('#live-edit-stop');

            this.updated_warning = $('#updated-warning');
        },
        initActions: function() {
            this.save_btn.click($.proxy(this.proceedSave, this));

            this.edit_start_btn.click($.proxy(this.startEditing, this));
            this.edit_stop_btn.click($.proxy(this.stopEditing, this));

            this.selectedContent = null;

            var self = this;

            // focus out simpletext
            this.inline_edit.focusin(function() {
                self.selectedContent = $(this).html();
            }).focusout(function() {
                var $this = $(this);
                // selected content stayed the same, do not save
                if(self.selectedContent == $this.html())
                    return;
                if(!$this.hasClass('tinymce'))
                    $this.html(self.stripTag($this.html()));
                self.proceedSave();
                if(!$this.text() || $this.text() === '')
                    $this.html('<span class="live-edit-empty">empty<span>');
                self.selectedContent = null;
            });

            this.has_been_modified = false;
            this.contenttypes_edit_btns.click($.proxy(function() {
                this.has_been_modified = true;
                this.showUpdatedWarning();
            }, this));


            // lightbox close
            this.lightbox_container.find('.cancel').click(function(event) {
                event.preventDefault();
                self.cancelLightBox();
            });

            // lightbox save
            this.lightbox_container.find('.save').click(function(event) {
                event.preventDefault();
                self.saveRichtext();
                self.cancelLightBox();
            });

            this.richtext_edit.click(function() {
                event.preventDefault();
                self.active_anchor = $(this).attr('data-anchor');
                self.openLightBox();
            });
        },
        startEditing: function() {
            this.inline_edit.attr('contenteditable', 'true').addClass('marked-editable');
            this.richtext_edit.addClass('marked-editable');
            this.contenttypes_edit_btns.show();
            this.edit_start_btn.hide();
            this.edit_stop_btn.show();

            tinymce.init(window.tinymce_inline_config);
        },
        stopEditing: function() {
            this.inline_edit.attr('contenteditable', 'false').removeClass('marked-editable');
            this.richtext_edit.removeClass('marked-editable');
            this.contenttypes_edit_btns.hide();
            this.edit_start_btn.show();
            this.edit_stop_btn.hide();

            tinymce.remove('span.tinymce.inline');
        },
        proceedSave: function() {
            var simple_text_list = '';
            this.inline_edit.each($.proxy(function(key, value) {
                var $value = $(value);
                var stripped_tring = $value.html();
                if(!$value.hasClass('tinymce'))
                    stripped_tring = this.stripTag($value.html());
                simple_text_list += $value.attr('data-anchor') + "=" + escape(stripped_tring) + '&';
            }, this));

            // prepare richtext
            var richtext_text_list = '';
            this.richtext_edit.each($.proxy(function(key, value) {
                var $value = $(value);
                simple_text_list += $value.attr('data-anchor') + "=" + escape($value.html()) + '&';
            }, this));

            $.ajax({
                url: '/api/save/',
                method: 'POST',
                data: simple_text_list
            });
            this.showSaveView();
        },
        showSaveView: function() {
            if(!this.save_progress_view)
                this.save_progress_view = this.$panel.find('.save-progress');
            
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
        openLightBox: function() {
            this.lightbox_container.show();
            this.tinymce = tinymce.init(window.tinymce_config);
            tinymce.activeEditor.setContent($('[data-anchor="' + this.active_anchor + '"]').html());
        },
        cancelLightBox: function() {
            this.lightbox_container.hide();
        },
        saveRichtext: function() {
            $('[data-anchor="' + this.active_anchor + '"]').html(tinymce.activeEditor.getContent());
            this.proceedSave();
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