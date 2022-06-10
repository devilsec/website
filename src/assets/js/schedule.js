/**
 *
 * JS File for the Schedule page
 *
 */

var eventModal = document.getElementById('eventModal');
eventModal.addEventListener('show.bs.modal', function(event){
  // Retrieve all of the values passed to the modal:
  var button=event.relatedTarget;
  var name=button.getAttribute('data-bs-name');
  var date=button.getAttribute('data-bs-date');
  var time=button.getAttribute('data-bs-time');
  var loc=button.getAttribute('data-bs-loc');
  var locURL=button.getAttribute('data-bs-loc-url');
  var speakers=button.getAttribute('data-bs-speakers');
  var description=button.getAttribute('data-bs-desc');
  var icsURL=button.getAttribute('data-bs-ics-url');

  // Update the contents of the modal:
  var modalTitle=eventModal.querySelector('.modal-title');
  modalTitle.textContent=name;
  var modalDate=eventModal.querySelector('.modal-date');
  modalDate.textContent=date;
  var modalTime=eventModal.querySelector('.modal-time');
  modalTime.textContent=time;
  var modalLoc=eventModal.querySelector('.modal-loc');
  modalLoc.textContent=loc;
  var modalLocURL=eventModal.querySelector('.location-link');
  modalLocURL.href=locURL;
  var modalSpeakers=eventModal.querySelector('.modal-speakers');
  modalSpeakers.textContent=speakers;
  var modalDesc=eventModal.querySelector('.modal-description');
  modalDesc.textContent=description;
  var modalICS=eventModal.querySelector('.calendar-btn');
  modalICS.href=icsURL;
});
