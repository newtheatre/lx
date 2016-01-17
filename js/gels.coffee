---
---

GEL_TEMPLATE = "#gel-template"
GEL_CONTAINER = "#gels-list"
GEL_ELEMENTS = "#gels-list li"

GEL_DATA_CODE = "gel-code"
GEL_DATA_COLOR = "gel-color"
GEL_DATA_NAME = "gel-name"
GEL_DATA_DESCRIPTION = "gel-description"

SORT_BUTTONS = ".gel-sort-button"
SORT_NUMERIC = "#gel-sort-numeric"
SORT_HUE = "#gel-sort-hue"

FILTER_TEXT = "#q"

SORT_ACTIVE_CLASS = "active"

gel_lib = []
gel_sort = "sort"
gel_filter = ""

debounce = (fn) ->
  # prevents too many searches happening at once
  timeout = undefined
  ->
    args = Array::slice.call(arguments)
    ctx = this
    clearTimeout timeout
    timeout = setTimeout((->
      fn.apply ctx, args
      return
    ), 100)

rgb2hue = (r,g,b) ->
  # Formula from https://en.wikipedia.org/wiki/Hue, Frank Preucil 1953
  Math.atan2(Math.sqrt(3)*(g-b), 2*r-g-b)

display_gels = (gels, sort, filter, template) ->
  output = ""

  gels.sort (a, b) ->
    a[sort] - b[sort]

  filter = filter.toLowerCase()

  if filter != ""
    gels = gels.filter (a) ->
      a.code == filter or
      a.sort.toString() == filter or
      a.name.toLowerCase().search(filter) >= 0 or
      a.description.toLowerCase().search(filter) >= 0

  $(gels).each ->
    output += template({gel: @})

  $(GEL_CONTAINER).empty()
  $(GEL_CONTAINER).html(output)

$(document).ready ->
  # Parse DOM and extract gels
  $(GEL_ELEMENTS).each ->
    # slice RGB values and convert from hex to dec
    r = parseInt($(@).data(GEL_DATA_COLOR).slice(0,2), 16)
    g = parseInt($(@).data(GEL_DATA_COLOR).slice(2,4), 16)
    b = parseInt($(@).data(GEL_DATA_COLOR).slice(4,6), 16)

    # build gel object and push to array
    gel = {
      sort: $(@).data(GEL_DATA_CODE).slice(1),
      code: $(@).data(GEL_DATA_CODE),
      color: $(@).data(GEL_DATA_COLOR),
      hue: rgb2hue(r,g,b),
      name: $(@).data(GEL_DATA_NAME),
      description: $(@).data(GEL_DATA_DESCRIPTION),
    }
    gel_lib.push(gel)

  gel_template = _.template($(GEL_TEMPLATE).html())

  display_gels(gel_lib, gel_sort, gel_filter, gel_template)

  $(SORT_NUMERIC).click ->
    gel_sort = "sort"
    display_gels(gel_lib, gel_sort, gel_filter, gel_template)
    $(SORT_BUTTONS).removeClass(SORT_ACTIVE_CLASS)
    $(@).addClass(SORT_ACTIVE_CLASS)

  $(SORT_HUE).click ->
    gel_sort = "hue"
    display_gels(gel_lib, gel_sort, gel_filter, gel_template)
    $(SORT_BUTTONS).removeClass(SORT_ACTIVE_CLASS)
    $(@).addClass(SORT_ACTIVE_CLASS)

  $(FILTER_TEXT).keyup debounce ->
    gel_filter = $(@).val()
    display_gels(gel_lib, gel_sort, gel_filter, gel_template)

  window.gl = gel_lib
