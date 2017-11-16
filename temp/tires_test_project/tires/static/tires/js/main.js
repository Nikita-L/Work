function deleteTire(pk) {
    $('#detailsModal').modal('hide');
    angular.element(document.getElementById('ctrl')).scope().deleteTire(pk);
}
function add_or_edit() {
    $('form').submit();
}