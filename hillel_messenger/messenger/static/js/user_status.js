function fetchUserStatuses() {
    $.ajax({
        url: 'users/status/list/',
        method: 'GET',
        success: function(users) {
            const userStatusList = $('#user-status-list');
            userStatusList.empty();

            users.forEach(user => {
                const userDiv = $(`
                    <div>
                        <span>${user.name}</span>
                        <span class="status" style="color: ${user.is_online ? 'green' : 'red'};">
                            ${user.is_online ? 'Online' : 'Offline'}
                        </span>
                    </div>
                `);
                userStatusList.append(userDiv);
            });
        },
        error: function(error) {
            console.error('Ошибка при получении статусов пользователей:', error);
        }
    });
}

setInterval(fetchUserStatuses, 5000);

fetchUserStatuses();
