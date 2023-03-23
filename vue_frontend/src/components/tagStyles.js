
export function getClasses(t) {
    // console.log("getClasses has ", t)
    var base = "avenir f6 link dim br-pill ph2 pv mv1 dib white".split(' ')
    var type = (typeof(t) == 'string')? t : t.type
    // console.log(typeof(t), type, t instanceof String)
    switch (type) {
        case "mp3":
            return [...base, 'bg-gold-8'];
        case "cantor":
            return [...base, 'bg-violet-2'];
        case "piano":
            return [...base, 'bg-green-8']
        case "guitar":
            return [...base, 'bg-green-5'];
        case "melody":
            return [...base, 'bg-blue-4'];
        case "harmony":
            return [...base, 'bg-red-3'];
        case "soprano":
            return [...base, 'bg-teal-2'];
        case "alto":
            return [...base, 'bg-teal-5'];
        case "tenor":
            return [...base, 'bg-teal-7'];
        case "bass":
            return [...base, 'bg-teal-9'];
        case "Powerpoint":
            return [...base, 'bg-red-6'];
        default:
            return [...base, 'bg-gray-4'];
    }
}
 