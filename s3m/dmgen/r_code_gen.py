# -*- coding: utf-8 -*-
# Copyright, 2014-2015 - Timothy W. Cook <tim@mlhim.org>. All Rights Reserved.
# Generate source code for data analysis using the R language system.
from datetime import datetime, date
from xml.sax.saxutils import unescape

now = date.today()
year = str(now.timetuple()[0])

def pct_rcode(self, pcmType):
    ct_id = self.ct_id
    label = self.label
    rstr = '' #The string to write to each PcT
    r_name = ''.join(e for e in label if e.isalnum())  # replace all special characters.
    rstr += "# Copyright "+year+", Timothy W. Cook <tim@mlhim.org>\n"
    rstr += "# Licensed under the Apache License, Version 2.0 (the 'License');\n"
    rstr += "# you may not use this file except in compliance with the License.\n"
    rstr += "# You may obtain a copy of the License at\n"
    rstr += "# http://www.apache.org/licenses/LICENSE-2.0\n"
    rstr += "\n"
    rstr += "# Unless required by applicable law or agreed to in writing, software\n"
    rstr += "# distributed under the License is distributed on an 'AS IS' BASIS,\n"
    rstr += "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
    rstr += "# See the License for the specific language governing permissions and\n"
    rstr += "# limitations under the License.\n"
    rstr += "#' \code{"+label.strip()+".}\n"
    rstr += "#'\n"
    rstr += "#' Returns a data.frame of the collected nodes of: \code{"+label.strip()+"} from the XML instance passed as fileName.\n"
    rstr += "#' The source name and the CCD ID are also included in each row to assist in identifying the source of the data.\n"
    rstr += "#' The XML element name is pcs-"+ct_id+" as a restriction of the "+pcmType+"\n"
    # add the list of vectors to the documentation
    rstr += "#' The vectors are: label, vtb, vte, "
    if pcmType == 'XdBoolean':
        rstr += "#' true_value, false_value, "
    elif pcmType == 'XdLink':
        rstr += "#' link, relation, relation_uri, "
    elif pcmType == 'XdString':
        rstr += "#' Xdstring_value, Xdstring_language, "
    elif pcmType == 'XdFile':
        rstr += "#' size, encoding, Xdfile_language, media_type, compression_type, hash_result, hash_function, alt_txt, uri, media_content, text_content, "
    elif pcmType == 'XdOrdinal':
        rstr += "#' normal_status, ordinal, symbol, rr_label, rr_definition, rr_vtb, rr_vtb, rr_is_normal, interval_label, interval_lower, interval_upper, lower_included, upper_included, lower_bounded, upper_bounded, "
    elif pcmType == 'XdCount':
        rstr += "#' normal_status, Xdcount_value,  units_value, units_label,  rr_label, rr_definition, rr_vtb, rr_vtb, rr_is_normal, interval_label, interval_lower, interval_upper, lower_included, upper_included, lower_bounded, upper_bounded, "
    elif pcmType == 'XdTemporal':
        rstr += "#' normal_status,  rr_label, rr_definition, rr_vtb, rr_vtb, rr_is_normal, interval_label, interval_lower, interval_upper, lower_included, upper_included, lower_bounded, upper_bounded, "
        rstr += "#' One or more of: Xdtemporal_date, Xdtemporal_time, Xdtemporal_datetime, Xdtemporal_datetime_stamp, Xdtemporal_day, Xdtemporal_month, Xdtemporal_year, Xdtemporal_year_month, Xdtemporal_month_day, Xdtemporal_duration, Xdtemporal_ymduration, Xdtemporal_dtduration\n"
    elif pcmType == 'XdQuantity':
        rstr += "#' normal_status, Xdquantity_value, magnitude_status, error, accuracy, units_value, units_label,  rr_label, rr_definition, rr_vtb, rr_vtb, rr_is_normal, interval_label, interval_lower, interval_upper, lower_included, upper_included, lower_bounded, upper_bounded, "
    elif pcmType == 'XdRatio':
        rstr += "#' normal_status, Xdratio_value, magnitude_status, error, accuracy, ratio_type, numerator, denominator, numerator_units, numerator_units_label, denominator_units, denominator_units_label, ratio_units,  rr_label, rr_definition, rr_vtb, rr_vtb, rr_is_normal, interval_label, interval_lower, interval_upper, lower_included, upper_included, lower_bounded, upper_bounded, "

    rstr += "#' ccd, sourceName,\n"
    rstr += "#' \n"
    descr = self.description.splitlines()
    for n in range(0, len(descr)):
        rstr += "#' "+descr[n]+"\n"
    rstr += "#' \n"
    rstr += "#' @references\n"
    rstr += "#' The data is structured according to the Multi-Level Healthcare Information Modelling Reference Model release 2.5.0\n"
    rstr += "#' \\url{http://www.mlhim.org}\n"
    rstr += "#' The semantic reference(s) for this data:\n"
    rstr += "#' @references\n"

    # rstr += "#' \\code{"+self.predicate.__str__()+"} \\url{"+unescape(self.object_uri)+"} and can be accessed via the CCD. A CCD is an XML Schema with embeded RDF.\n"

    rstr += "#' \n"
    rstr += "#' @param fileList - The path/file name(s) of the XML file(s) to process.\n"
    rstr += "#' @return A dataframe consisting of the vectors listed in the Description.\n"
    rstr += "#' \n"
    rstr += "#' The examples use the included files. Any source that can be processed via the XML::xmlTreeParse function can be used.\n"
    rstr += "#' @examples\n"
    rstr += "#' files <- dir('./inst/examples', recursive=TRUE, full.names=TRUE, pattern='\\\.xml$')\n"
    rstr += "#' "+r_name+" <- get"+r_name+"(files) \n"
    rstr += "#' \n"
    rstr += "#' @export\n"
    rstr += "get"+r_name+" <- function(sourceList)\n"
    rstr += "{\n"
    rstr += "    data <- lapply(sourceList, parse"+r_name+")\n"
    rstr += "    data <- data.table::rbindlist(data, fill=TRUE)\n"
    rstr += "    return(data)\n"
    rstr += "}\n"
    rstr += "\n"
    rstr += "#' @export\n"
    rstr += "parse"+r_name+" <- function(sourceName) {\n"
    rstr += "  nsDEF <- c(mlhim2='http://www.mlhim.org/ns/mlhim2/', xsi='http://www.w3.org/2001/XMLSchema-instance')\n"
    rstr += "  doc <- XML::xmlTreeParse(sourceName, handlers=list('comment'=function(x,...){NULL}), asTree = TRUE)\n"
    rstr += "  root <- XML::xmlRoot(doc)\n"
    rstr += "  pcm <- XML::getNodeSet(root, '//mlhim2:pcs-"+ct_id+"', nsDEF)\n"
    rstr += "  data <- lapply(pcm, mlhim250rm::"+pcmType+")\n"
    rstr += "  data <- data.table::rbindlist(data, fill=TRUE)\n"
    rstr += "  if (length(data) > 0) { \n"
    rstr += "      data$ccd <- XML::xmlName(root)\n"
    rstr += "      data$pcs <- 'pcs-"+ct_id+"'\n"
    rstr += "      data$ccd <- XML::xmlName(root)\n"
    rstr += "      data$sourceName <- sourceName\n"
    rstr += " } else {\n"
    rstr += "    data <- data.frame()\n"
    rstr += "  }\n"
    rstr += " return(data)\n"
    rstr += "}\n"

    return(rstr)
