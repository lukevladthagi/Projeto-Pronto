
"use strict";
var KTAppCalendar = function() {
    var e, t, n, a, o, r, i, l, d, c, s, m, u, v, f, p, y, D, k, _, g, b, S, h, T, Y, w, L, E, M = {
        id: "",
        eventName: "",
        eventDescription: "",
        eventLocation: "",
        startDate: "",
        endDate: "",
        allDay: !1
    };
    const x = () => {
            v.innerText = "Add a New Event", u.show();
            C(M), D.addEventListener("submit", (function(o) {
                o.preventDefault(), p && p.validate().then((function(o) {
                    console.log("validated!"), "Valid" == o ? (D.setAttribute("data-kt-indicator", "on"), D.disabled = !0, setTimeout((function() {
                        D.removeAttribute("data-kt-indicator"), Swal.fire({
                            text: "New event added to calendar!",
                            icon: "success",
                            buttonsStyling: !1,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        }).then((function(o) {
                            if (o.isConfirmed) {
                                u.hide(), D.disabled = !1;
                                let o = !1;
                                i.checked && (o = !0), 0 === c.selectedDates.length && (o = !0);
                                var d = moment(r.selectedDates[0]).format(),
                                    s = moment(l.selectedDates[l.selectedDates.length - 1]).format();
                                if (!o) {
                                    const e = moment(r.selectedDates[0]).format("YYYY-MM-DD"),
                                        t = e;
                                    d = e + "T" + moment(c.selectedDates[0]).format("HH:mm:ss"), s = t + "T" + moment(m.selectedDates[0]).format("HH:mm:ss")
                                }
                                e.addEvent({
                                    id: A(),
                                    title: t.value,
                                    description: n.value,
                                    location: a.value,
                                    start: d,
                                    end: s,
                                    allDay: o
                                }), e.render(), f.reset()
                            }
                        }))
                    }), 2e3)) : Swal.fire({
                        text: "Sorry, looks like there are some errors detected, please try again.",
                        icon: "error",
                        buttonsStyling: !1,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    })
                }))
            }))
        },
        B = () => {
            var e, t, n;
            w.show(), M.allDay ? (e = "All Day", t = moment(M.startDate).format("Do MMM, YYYY"), n = moment(M.endDate).format("Do MMM, YYYY")) : (e = "", t = moment(M.startDate).format("Do MMM, YYYY - h:mm a"), n = moment(M.endDate).format("Do MMM, YYYY - h:mm a")), g.innerText = M.eventName, b.innerText = e, S.innerText = M.eventDescription ? M.eventDescription : "--", h.innerText = M.eventLocation ? M.eventLocation : "--", T.innerText = t, Y.innerText = n
        },
        q = () => {
            L.addEventListener("submit", (o => {
                o.preventDefault(), w.hide(), (() => {
                    v.innerText = "Edit an Event", u.show();
                    C(M), D.addEventListener("submit", (function(o) {
                        o.preventDefault(), p && p.validate().then((function(o) {
                            console.log("validated!"), "Valid" == o ? (D.setAttribute("data-kt-indicator", "on"), D.disabled = !0, setTimeout((function() {
                                D.removeAttribute("data-kt-indicator"), Swal.fire({
                                    text: "New event added to calendar!",
                                    icon: "success",
                                    buttonsStyling: !1,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn btn-primary"
                                    }
                                }).then((function(o) {
                                    if (o.isConfirmed) {
                                        u.hide(), D.disabled = !1, e.getEventById(M.id).remove();
                                        let o = !1;
                                        i.checked && (o = !0), 0 === c.selectedDates.length && (o = !0);
                                        var d = moment(r.selectedDates[0]).format(),
                                            s = moment(l.selectedDates[l.selectedDates.length - 1]).format();
                                        if (!o) {
                                            const e = moment(r.selectedDates[0]).format("YYYY-MM-DD"),
                                                t = e;
                                            d = e + "T" + moment(c.selectedDates[0]).format("HH:mm:ss"), s = t + "T" + moment(m.selectedDates[0]).format("HH:mm:ss")
                                        }
                                        e.addEvent({
                                            id: A(),
                                            title: t.value,
                                            description: n.value,
                                            location: a.value,
                                            start: d,
                                            end: s,
                                            allDay: o
                                        }), e.render(), f.reset()
                                    }
                                }))
                            }), 2e3)) : Swal.fire({
                                text: "Sorry, looks like there are some errors detected, please try again.",
                                icon: "error",
                                buttonsStyling: !1,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            })
                        }))
                    }))
                })()
            }))
        },
        N = e => {
            M.id = e.id, M.eventName = e.title, M.eventDescription = e.description, M.eventLocation = e.location, M.startDate = e.startStr, M.endDate = e.endStr, M.allDay = e.allDay
        },
        A = () => Date.now().toString() + Math.floor(1e3 * Math.random()).toString();
    return {
        init: function() {
            let events = [];
            const C = document.getElementById("kt_modal_add_event");
            f = C.querySelector("#kt_modal_add_event_form"), t = f.querySelector('[name="calendar_event_name"]'), n = f.querySelector('[name="calendar_event_description"]'), a = f.querySelector('[name="calendar_event_location"]'), o = f.querySelector("#kt_calendar_datepicker_start_date"), i = f.querySelector("#kt_calendar_datepicker_end_date"), d = f.querySelector("#kt_calendar_datepicker_start_time"), s = f.querySelector("#kt_calendar_datepicker_end_time"), y = document.querySelector('[data-kt-calendar="add"]'), D = f.querySelector("#kt_modal_add_event_submit"), k = f.querySelector("#kt_modal_add_event_cancel"), _ = C.querySelector("#kt_modal_add_event_close"), v = f.querySelector('[data-kt-calendar="title"]'), u = new bootstrap.Modal(C);
            const H = document.getElementById("kt_modal_view_event");
            var F, O, I, R, V, P;
            w = new bootstrap.Modal(H), g = H.querySelector('[data-kt-calendar="event_name"]'), b = H.querySelector('[data-kt-calendar="all_day"]'), S = H.querySelector('[data-kt-calendar="event_description"]'), h = H.querySelector('[data-kt-calendar="event_location"]'), T = H.querySelector('[data-kt-calendar="event_start_date"]'), Y = H.querySelector('[data-kt-calendar="event_end_date"]'), L = H.querySelector("#kt_modal_view_event_edit"), E = H.querySelector("#kt_modal_view_event_delete"), F = document.getElementById("kt_calendar_app"), O = moment().startOf("day"), I = O.format("YYYY-MM"), R = O.clone().subtract(1, "day").format("YYYY-MM-DD"), V = O.format("YYYY-MM-DD"), P = O.clone().add(1, "day").format("YYYY-MM-DD"), (e = new FullCalendar.Calendar(F, {
                headerToolbar: {
                    left: "prev,next today",
                    center: "title",
                    right: "dayGridMonth,timeGridWeek,timeGridDay"
                },
                initialDate: V,
                navLinks: !0,
                selectable: !0,
                selectMirror: !0,
                select: function(e) {
                    N(e), x()
                },
                eventClick: function(e) {
                    N({
                        id: e.event.id,
                        title: e.event.title,
                        description: e.event.extendedProps.description,
                        location: e.event.extendedProps.location,
                        startStr: e.event.startStr,
                        endStr: e.event.endStr,
                        allDay: e.event.allDay
                    }), B()
                },
                editable: !0,
                dayMaxEvents: !0,
                
                events: [],

                datesSet: function() {}
            })).render(), p = FormValidation.formValidation(f, {
                fields: {
                    calendar_event_name: {
                        validators: {
                            notEmpty: {
                                message: "Event name is required"
                            }
                        }
                    },
                    calendar_event_start_date: {
                        validators: {
                            notEmpty: {
                                message: "Start date is required"
                            }
                        }
                    },
                    calendar_event_end_date: {
                        validators: {
                            notEmpty: {
                                message: "End date is required"
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger,
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: ".fv-row",
                        eleInvalidClass: "",
                        eleValidClass: ""
                    })
                }
            }), r = flatpickr(o, {
                enableTime: !1,
                dateFormat: "Y-m-d"
            }), l = flatpickr(i, {
                enableTime: !1,
                dateFormat: "Y-m-d"
            }), c = flatpickr(d, {
                enableTime: !0,
                noCalendar: !0,
                dateFormat: "H:i"
            }), m = flatpickr(s, {
                enableTime: !0,
                noCalendar: !0,
                dateFormat: "H:i"
            }), q(), y.addEventListener("submit", (e => {
                M = {
                    id: "",
                    eventName: "",
                    eventDescription: "",
                    startDate: new Date,
                    endDate: new Date,
                    allDay: !1
                }, x()
            })), E.addEventListener("submit", (t => {
                t.preventDefault(), Swal.fire({
                    text: "Are you sure you would like to delete this event?",
                    icon: "warning",
                    showCancelButton: !0,
                    buttonsStyling: !1,
                    confirmButtonText: "Yes, delete it!",
                    cancelButtonText: "No, return",
                    customClass: {
                        confirmButton: "btn btn-primary",
                        cancelButton: "btn btn-active-light"
                    }
                }).then((function(t) {
                    t.value ? (e.getEventById(M.id).remove(), w.hide()) : "cancel" === t.dismiss && Swal.fire({
                        text: "Your event was not deleted!.",
                        icon: "error",
                        buttonsStyling: !1,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    })
                }))
            })), k.addEventListener("submit", (function(e) {
                e.preventDefault(), Swal.fire({
                    text: "Are you sure you would like to cancel?",
                    icon: "warning",
                    showCancelButton: !0,
                    buttonsStyling: !1,
                    confirmButtonText: "Yes, cancel it!",
                    cancelButtonText: "No, return",
                    customClass: {
                        confirmButton: "btn btn-primary",
                        cancelButton: "btn btn-active-light"
                    }
                }).then((function(e) {
                    e.value ? (f.reset(), u.hide()) : "cancel" === e.dismiss && Swal.fire({
                        text: "Your form has not been cancelled!.",
                        icon: "error",
                        buttonsStyling: !1,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    })
                }))
            })), _.addEventListener("submit", (function(e) {
                e.preventDefault(), Swal.fire({
                    text: "Are you sure you would like to cancel?",
                    icon: "warning",
                    showCancelButton: !0,
                    buttonsStyling: !1,
                    confirmButtonText: "Yes, cancel it!",
                    cancelButtonText: "No, return",
                    customClass: {
                        confirmButton: "btn btn-primary",
                        cancelButton: "btn btn-active-light"
                    }
                }).then((function(e) {
                    e.value ? (f.reset(), u.hide()) : "cancel" === e.dismiss && Swal.fire({
                        text: "Your form has not been cancelled!.",
                        icon: "error",
                        buttonsStyling: !1,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    })
                }))
            })), (e => {
                e.addEventListener("hidden.bs.modal", (e => {
                    p && p.resetForm(!0)
                }))
            })(C)

            async function fetchEventsFromAPI() {
            try {
                const loader = document.getElementById("loader");
                loader.style.display = "block";
               
                const response = await fetch('http://127.0.0.1:8000/prontocardio/controle_agenda/api/events/');
                console.log('Fez o fetch aqui')
                if (!response.ok) {
                throw new Error('Erro ao buscar eventos da API: ' + response.status + ' ' + response.statusText);
                }
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('Erro na solicitação à API:', error);
                return []
            } finally {
                const loader = document.getElementById("loader");
                loader.style.display = "none";
            }
        }

            async function loadEventsFromAPI() {
            try {
                const apiEvents = await fetchEventsFromAPI();

                apiEvents.forEach((event) => {
                e.addEvent({
                    id: A(),
                    title: `[${event.idade}] - ` + event.nm_paciente,
                    description: event.ds_tip_mar,
                    location: `${event.nm_convenio} `,
                    start: event.hr_agenda, 
                    end:  event.hr_agenda, 
                    className: "fc-event-danger fc-event-solid-warning",
                });
                console.log(apiEvents);
        
                
                events.push({
                    id: A(),
                    title: `[${event.idade}] - ` + event.nm_paciente,
                    description: `Idade: ${event.idade} /  ${event.ds_tip_mar} `,
                    location: event.nm_convenio,
                    start: I + event.hr_agenda, 
                    end: I + event.hr_agenda,
                    className: "fc-event-danger fc-event-solid-warning",
                });
                });

            } catch (error) {
                console.error('Erro ao carregar eventos da API:', error);
            }
            console.log(events);
            }
        
         
            loadEventsFromAPI();
          
    }
}
}();
KTUtil.onDOMContentLoaded((function() {
    KTAppCalendar.init()
}));
