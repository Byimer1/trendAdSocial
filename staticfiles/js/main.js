$(document).ready(function() {
    // Like functionality
    $('.like-btn').click(function() {
        const postId = $(this).data('post-id');
        const button = $(this);
        
        $.post(`/${postId}/like/`, {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        })
        .done(function(response) {
            const icon = button.find('i');
            const count = button.find('.like-count');
            
            if (response.liked) {
                icon.removeClass('bi-heart').addClass('bi-heart-fill text-danger');
                count.text(parseInt(count.text()) + 1);
            } else {
                icon.removeClass('bi-heart-fill text-danger').addClass('bi-heart');
                count.text(parseInt(count.text()) - 1);
            }
        });
    });

    // Save post functionality
    $('.save-btn').click(function() {
        const postId = $(this).data('post-id');
        const button = $(this);
        
        $.post(`/${postId}/save/`, {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        })
        .done(function(response) {
            const icon = button.find('i');
            if (response.saved) {
                icon.removeClass('bi-bookmark').addClass('bi-bookmark-fill');
            } else {
                icon.removeClass('bi-bookmark-fill').addClass('bi-bookmark');
            }
        });
    });

    // Comment submission
    $('.comment-form').submit(function(e) {
        e.preventDefault();
        const form = $(this);
        const postId = form.data('post-id');
        const input = form.find('input[name=content]');
        
        $.post(`/${postId}/comment/`, {
            'content': input.val(),
            'csrfmiddlewaretoken': form.find('input[name=csrfmiddlewaretoken]').val()
        })
        .done(function(response) {
            const commentsList = form.siblings('.comments-list');
            commentsList.append(`
                <div class="comment">
                    <a href="/users/${response.username}/" class="fw-bold text-dark text-decoration-none">
                        ${response.username}
                    </a>
                    <span>${response.content}</span>
                    <small class="text-muted">Just now</small>
                </div>
            `);
            input.val('');
        });
    });

    // Check for unread notifications
    function checkUnreadNotifications() {
        $.get('/notifications/unread-count/')
        .done(function(response) {
            const badge = $('.unread-notifications-count');
            if (response.count > 0) {
                badge.text(response.count).show();
            } else {
                badge.hide();
            }
        });
    }

    // Check for unread messages
    function checkUnreadMessages() {
        $.get('/messages/unread-count/')
        .done(function(response) {
            const badge = $('.unread-messages-count');
            if (response.count > 0) {
                badge.text(response.count).show();
            } else {
                badge.hide();
            }
        });
    }

    // Check for notifications and messages every 30 seconds
    setInterval(function() {
        checkUnreadNotifications();
        checkUnreadMessages();
    }, 30000);

    // Initial check
    checkUnreadNotifications();
    checkUnreadMessages();
}); 