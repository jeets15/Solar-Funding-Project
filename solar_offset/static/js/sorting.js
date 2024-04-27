/*
== How to use sorting.js ==

1.) Specify a container whose children will be sorted
      To do this, add the 'sorting-target' attribute to the container and give it a unique id for this page
      e.g. sorting-target="my-list"
2.) Create a number of buttons that work as your sorting options (e.g. using a bootstrap dropdown)
      For each sorting option, add the following attributes
      - sorting-option="your-sorting-target-id"
      - sorting-key="the sort key"
3.) (Optional) If you want to toggle between ascending and descending add another button somewhere on your page
      Give it the sorting-direction="your-sorting-target-id" attribute
      The sort direction can be toggled if you specify sorting-asc and sorting-desc on two of its child attributes
      whose content can be shown selectively
      if you want to choose a default sort direction then set sorting-direction-default to either "asc" or "desc"
      (ascending is the default)
4.) For each child item in your target container, and for each sorting key,
      add the sorting-key attribute to one html element inside the child container
      - the innerHTML value of this element will be used to sort by that key
5.) If you want your sort options to appear only once this script has been loaded
      add the sorting-hidden="display: the-normal-display type" attribute
      and the display:none style to hide them until this script is ready
6.) any element with the sorting-current="your-sorting-target-id"
      will have its inner HTML replaced any time a new sort option is selected
*/

const urlParams = new URL(window.location).searchParams;

function sortingUrlEncode(obj) {
    let sortings = []
    for (let id in obj) {
        let key = obj[id]['key'];
        let order = obj[id]['order'];
        sortings.push(`${id}*${key}*${order}`);
    }
    return encodeURIComponent(sortings.join("|"));
}

function filterCountries() {
    const query = document.getElementById('country-search').value.toLowerCase();
    const countryList = document.querySelectorAll('ul[sorting-target="country-list"] > li');

    countryList.forEach(country => {
        const countryName = country.querySelector('h3').textContent.toLowerCase();

        // Check if the country name contains the search query
        if (countryName.includes(query)) {
            country.style.display = 'block'; // Show the country if it matches the query
        } else {
            country.style.display = 'none'; // Hide the country if it doesn't match the query
        }
    });
}
function sortingUrlDecode(str) {
    let obj = {};
    if (!str) {
        return obj;
    }
    for (let sortString of decodeURIComponent(str).split("\|")) {
        let comps = sortString.split("\*");
        let id = comps[0];
        let key = comps[1];
        let order = comps[2];
        obj[id] = {'key': key, 'order': order};
    }
    return obj;
}

function isNumeric(str) {
    if (typeof str != 'string') {
        return false;
    } else {
        return !isNaN(str) && !isNaN(parseFloat(str)) && !isNaN(+str);
    }
  }

function triggerSort(targetId, sortKey, writeToUrlParams) {
    let order = $(`[sorting-direction=${targetId}]`).first().attr("sorting-direction-val");

    // Update elements with sorting-current attributes
    let sortKeyText = $(`[sorting-option=${targetId}][sorting-key=${sortKey}]`).first().html();
    $(`[sorting-current=${targetId}]`).html(sortKeyText);

    // update url parameters
    if (writeToUrlParams) {
        let url = new URL(window.location);
        let sortObj = sortingUrlDecode(url.searchParams.get('sort'));
        sortObj[targetId] = {'key': sortKey, 'order': order};
        url.searchParams.set('sort', sortingUrlEncode(sortObj));
        window.history.pushState(null, '', url);
    }

    // Change active sort option
    $(`[sorting-option=${targetId}]`).removeClass("active");
    $(`[sorting-option=${targetId}][sorting-key=${sortKey}]`).first().addClass("active");

    // Collecting elements that will be sorted and sort values
    // Are we allowed to do numerical comparisons
    // Or do we have to rely on string comparison
    // numCompare will remain true only if all values can be converted to a number
    let numCompare = true;
    let sortList = [];
    $(`[sorting-target=${targetId}`).first().children().each((_, el) => {
        let sortVal = $(el).find(`[sorting-key=${sortKey}]`).first().html();
        sortList.push([el, sortVal]);
        if (!isNumeric(sortVal)) {
            numCompare = false;
        }
    });

    // Do actual sorting
    let mult = (order === "desc") ? -1 : 1;
    sortList.sort((a, b) => {
        let aVal = a[1];
        let bVal = b[1];
        if (numCompare) {
            aVal = +aVal;
            bVal = +bVal;
        }
        if (aVal < bVal) {
            return -1 * mult;
        } else if (aVal > bVal) {
            return 1 * mult;
        } else {
            return 0;
        }
    });

    // Apply the re-ordered elements to the container
    let children = sortList.map((x) => x[0]);
    $(`[sorting-target=${targetId}`).first().get(0).replaceChildren(...children);
}

// Register Actions to allow sorting
$('[sorting-target]').each((_, el) => {
    let id = $(el).attr("sorting-target");


    // Register sort order button
    let sortButtonStr = `[sorting-direction=${id}]`;
    let sortAscHtml = $(`[sorting-direction=${id}] [sorting-asc]`).first().html();
    let sortDescHtml = $(`[sorting-direction=${id}] [sorting-desc]`).first().html();
    let toggleToAsc = () => {
        $(sortButtonStr).first().attr("sorting-direction-val", "asc");
        $(sortButtonStr).first().html(sortAscHtml);
    };
    let toggleToDesc = () => {
        $(sortButtonStr).first().attr("sorting-direction-val", "desc");
        $(sortButtonStr).first().html(sortDescHtml);
    };
    if ($(sortButtonStr).first().attr("sorting-direction-default") === "desc") {
        toggleToDesc()
    } else {
        toggleToAsc();
    }
    $(sortButtonStr).first().on("click", () => {
        if ("asc" === $(sortButtonStr).first().attr("sorting-direction-val")) {
            toggleToDesc();
        } else if ("desc" === $(sortButtonStr).first().attr("sorting-direction-val")) {
            toggleToAsc()
        }
        triggerSort(id, $(`.active[sorting-option=${id}]`).first().attr("sorting-key"), true);
    });


    // Register sort option buttons
    $(`[sorting-option=${id}]`).each((_, el) => {
        let sortKey = $(el).attr("sorting-key");
        $(el).on("click", () => {triggerSort(id, sortKey, true)});
    });

    // Set initial default sort order
    $(`[sorting-option=${id}]`).first().addClass("active");

    // Check if a sort order exists for this target in the url options
    // Otherwise Sort per the first sort option
    if (id in sortingUrlDecode(urlParams.get('sort'))) {
        let idData = sortingUrlDecode(urlParams.get('sort'))[id];
        let _key = idData['key'];
        let _order = idData['order'];
        if (_order === "desc") {
            toggleToDesc();
        } else {
            toggleToAsc();
        }
        triggerSort(id, _key);
    } else {
        // Sort is triggered automatically when this is clicked
        triggerSort(id, $(`[sorting-option=${id}]`).first().attr('sorting-key'));
        // $(sortButtonStr).first().trigger("click");
    }
});

// Unhide sorting-hidden containers
$('[sorting-hidden]').each((_, el) => {
    let displayVal = $(el).attr('sorting-hidden');
    $(el).css("display", displayVal);
});