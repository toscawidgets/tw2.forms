import operator
import tw2.core as twc

NoDefault = object()

__all__ = ["DataGrid", "Column"]


class Column(object):
    """Simple struct that describes a single DataGrid column.

    Column has:
      - a name, which allows to uniquely identify a column in a DataGrid
      - a getter, which is used to extract the field's value
      - a title, which is displayed in the table's header
      - options, which is a way to carry arbitrary user-defined data

    """

    def __init__(self, name, getter=None, title=None, options=None):
        if not name:
            raise ValueError('name is required')

        if getter:
            if callable(getter):
                self.getter = getter
            else:  # assume it's an attribute name
                self.getter = operator.attrgetter(getter)
        else:
            self.getter = operator.attrgetter(name)
        self.name = name
        self.title = title is None and name.capitalize() or title
        self.options = options or {}

    def get_option(self, name, default=NoDefault):
        if name in self.options:
            return self.options[name]
        if default is NoDefault:  # no such key and no default is given
            raise KeyError(name)
        return default

    def get_field(self, row, displays_on=None):
        if getattr(self.getter, '__bases__', None) and \
           issubclass(self.getter, twc.Widget) or \
           isinstance(self.getter, twc.Widget):
            return self.getter.display(value=row, displays_on=displays_on)
        return self.getter(row)

    def __str__(self):
        return "<Column %s>" % self.name


class DataGrid(twc.Widget):
    """Generic widget to present and manipulate data in a grid (tabular) form.

    The columns to build the grid from are specified with fields constructor
    argument which is a list. An element can be a Column, an accessor
    (attribute name or function), a tuple (title, accessor) or a tuple
    (title, accessor, options).

    You can specify columns' data statically, via fields constructor parameter,
    or dynamically, via 'fields' key.

    """
    resources = [
        twc.CSSLink(modname='tw2.forms',
                    filename='static/datagrid/datagrid.css')
    ]
    template = "tw2.forms.templates.datagrid"
    css_class = 'grid'

    fields = twc.Param('Fields of the Grid', default=[], attribute=False)
    columns = twc.Variable('Used internally', default=[])

    @staticmethod
    def get_field_getter(columns):
        """Return a function to access the fields of table by row, col."""
        idx = {}  # index columns by name
        for col in columns:
            idx[col.name] = col

        def _get_field(row, col):
            return idx[col].get_field(row)

        return _get_field

    def _parse(self, fields):
        """Parse field specifications into a list of Columns.

        A specification can be a Column,
        an accessor (attribute name or function), a tuple (title, accessor)
        or a tuple (title, accessor, options).

        """
        columns = []
        names = {}  # keep track of names to ensure there are no dups
        for n, col in enumerate(fields):
            if not isinstance(col, Column):
                if isinstance(col, str) or callable(col):
                    name_or_f = col
                    title = options = None
                else:
                    title, name_or_f = col[:2]
                    try:
                        options = col[2]
                    except IndexError:
                        options = None
                # construct name using column index
                name = 'column-' + str(n)
                col = Column(name, name_or_f, title, options)
            if col.name in names:
                raise ValueError('Duplicate column name: %s' % col.name)
            columns.append(col)
            names[col.name] = 1
        return columns

    def prepare(self):
        super(DataGrid, self).prepare()

        if self.value is None:
            raise ValueError(
                "DataGrid must be passed a value.")

        if not self.fields and not self.columns:
            raise ValueError(
                "DataGrid must be passed either fields or columns")

        if self.fields:
            self.columns = self._parse(self.fields)

        self.get_field = self.get_field_getter(self.columns)
