export function containersChanged (a, b) {
    return containerPageIds(a).join() != containerPageIds(b).join();
}

function containerPageIds(a) {
    return a.map(function(c) {
        return c.getAttribute("page-id");
    });
}

export function containerHasInstance (c) {
    return c.children.length > 0;
}
