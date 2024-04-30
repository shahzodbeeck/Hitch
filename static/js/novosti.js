function iks() {
    const cancel = document.querySelector('.iks')
    const added = document.querySelector('.plused')
    const madalni = document.querySelector('.madalni')
    cancel.addEventListener('click', () => {
        madalni.style.visibility = `hidden`
    })
    added.addEventListener('click', () => {
        madalni.style.visibility = `visible`
    })
}

iks()
