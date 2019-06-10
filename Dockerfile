#	LICENSE NOTICE

# charcoalAPI - IoT server-less API for Edge devices
# Copyright (C) 2019 Anwesh Anjan Patel

# This file is part of charcoalAPI.

# charcoalAPI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# charcoalAPI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with charcoalAPI.  If not, see <https://www.gnu.org/licenses/>.

FROM python:3.6-alpine

WORKDIR /app

COPY ./requirements.txt /app

RUN apk add figlet

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Display warranty information and terms and conditions
RUN echo -e '#!/bin/sh\ncat /app/warranty\necho " "' > /usr/bin/warranty && \
	chmod +x /usr/bin/warranty && \
	echo -e '#!/bin/sh\ncat /app/LICENSE\necho " "' > /usr/bin/tnc && \
	chmod +x /usr/bin/tnc && \
	echo -e '#!/bin/sh\nsh /app/message.sh' > /usr/bin/info && \
	chmod +x /usr/bin/info

EXPOSE 8080

ENV NAME usn

CMD ["sh","start.sh"]