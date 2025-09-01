

document.addEventListener('DOMContentLoaded', function() {

    const fixScheduleButton = document.getElementById('fix-schedule-btn');

    if (fixScheduleButton) {

        fixScheduleButton.addEventListener('click', function(event) {
            
            event.preventDefault(); 
            
            window.location.href = 'Dashboard.html';
        });
    }

});