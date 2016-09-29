# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2016 CERN.
#
# INSPIRE is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Orcid serializer for records."""

from __future__ import absolute_import, print_function

from flask import current_app, jsonify

from invenio_orcid.utils import convert_to_orcid

from werkzeug import cached_property, import_string


class ORCIDSerializer(object):
    """Orcid serializer for records."""

    @cached_property
    def convert_to_orcid(self):
        """Import the orcid converter."""
        return import_string(
            current_app.config['ORCID_JSON_CONVERTER_MODULE'])

    def serialize(self, pid, record, links_factory=None):
        """Serialize a single orcid from a record.

        :param pid: Persistent identifier instance.
        :param record: Record instance.
        :param links_factory: Factory function for the link generation,
                              which are added to the response.
        """
        return jsonify(convert_to_orcid(record.dumps()))

    def serialize_search(self, pid_fetcher, search_result, links=None,
                         item_links_factory=None):
        """Serialize a search result.

        :param pid_fetcher: Persistent identifier fetcher.
        :param search_result: Elasticsearch search result.
        :param links: Dictionary of links to add to response.
        """
        records = []
        for hit in search_result['hits']['hits']:
            records.append(jsonify((convert_to_orcid(hit['_source']))))

        return "\n".join(records)
