# Return code definition for zVM SDK
#
# Copyright 2017 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


"""
Each error corresponds to a dictionary contains: 'overallRC', 'modID', 'rc',
'rs'.
-- 'overallRC' is used to indicate the overall return code, all the errors are
    classified into group with different overallRC value.

-- 'modID' is used to indicate which module this error happens in. The
    available Module and their modID value to use is listed in the following:

    ModName    ModID
    ------     --
    SMUT       1
    GUEST      10
    NETWORK    20
    VOLUME     30
    IMAGE      40
    MONITOR    50
    SDKSERVER  100
    SDKCLIENT  110
    SDKGENERAL 400

-- 'rc' is used together with rs to indicate the specific error. If 'rs' is
    enough to indicate the error, 'rc' would be set same to the overallRC.

-- 'rs' is used to indicate the specific error. It is defined specificly by
    each module. Different error inside a module should use different
    'rc'/'rs' combination.


-------------------------------------------------------------------------------
ErrorCode General Classification
-------------------------------------------------------------------------------
ErrorClass       overallRC modID  rc   rs    Description

SMUT               1-99     1     xx   xx    Used by SMUT, refer to
                                             smutlayer/msgs.py

Invalid input      100    SDKGEN  100   1    SDK API parameter number error
                   100    SDKGEN  100   2    SDK API input type error
                   100    SDKGEN  100   3    SDK API parameter format error (
                                              value not in expected format or
                                              range)

Socket Error       101    MODRC   101   x    The SDK server or client socket
                                             error.

Other Module Error 300    MODRC   300   x    The module-specific error during
                                             SDK API handling that not belongs
                                             to other general module-shared
                                             error.

Invalid API name   400    MODRC   400   x    The SDK server received a invalid
                                             API name.

Object Not Exist   404    MODRC   404   1    The operated object does not
                                             exist, eg, the guest/vswitch/
                                             image/volume.

Conflict           409    MODRC   409   x    The status of the to-be-updated
                                             object is conflict with the
                                             update request.

Object Deleted     410    MODRC   410   1    The operated object has been
                                             deleted and not exist any more.
                                             This can be used for some module
                                             that support deleted=1 in DB.

Internal error     500    MODRC   500   1    The SDK module got unexpected
                                             error, eg, typeerror, keyerror,
                                             etc. SDK  server would take all
                                             the exceptions not belonging to
                                             SDKBaseexception as InternalError
                                             .Such error generally means
                                             bug report, SDK code should avoid
                                             using this return code.

"""
# -----------------------------------------------------------------------------
# Detail Module RC definition of each error
# -----------------------------------------------------------------------------
ModRCs = {
    'smut': 1,
    'guest': 10,
    'network': 20,
    'volume': 30,
    'image': 40,
    'monitor': 50,
    'sdkserver': 100,
    'sdkclient': 110,
    # The 'zvmsdk' is used as the default module if module is not specified
    # when raising exception
    'zvmsdk': 400
    }

errors = {
    # Each entry defined here corresponds to a kind of error indicated by the
    # following list of info:
    # 1. the dict of 'overallRC', 'rc'
    # 2. the dict containing all the possible rs and its error message
    # 3. The general error description. This should be used for doc generation

# Invalid input error
    'input': [{'overallRC': 100, 'modID': ModRCs['zvmsdk'], 'rc': 100},
              {1: ("Invalid API arg count, API: %(api)s, %(expected)d expected"
                   " while %(provided)d provided."),
               2: ("Invalid API arg type, API: %(api)s, expected types: "
                   "'%(expected)s', input types: '%(inputtypes)s'"),
               3: ("Invalid API arg format, error: %(msg)s")
               },
              "Invalid API Input",
             ],
# SDK Client or Server socket error
# This error is not used by sdk exception, sdk client or server would set the
# 'modID' as the sdkserver or sdkclient module rc when got error, and use 'rs'
# as the socket error code.
    'socket': [{'overallRC': 101, 'modID': None, 'rc': 101},
               {},
               "SDK client or server get socket error",
               ],
# General Errors for each module, same overallRC = 300
# Guest Operation failed
    'guest': [{'overallRC': 300, 'modID': ModRCs['guest'], 'rc': 300},
              {1: "Database operation failed, error: %(msg)s",
               2: "Failed to add mdisks when creating guest, error: %(msg)s",
               3: ("Failed to deploy image to userid: '%(userid)s', "
                   "unpackdiskimage failed with rc: %(unpack_rc)d, "
                   "error: %(err)s"),
               4: ("Failed to deploy image to userid: '%(userid)s', "
                   "copy config drive to local failed with rc: %(cp_rc)d"),
              },
              "Operation on Guest failed"
              ],
# Network Operation failed
    'network': [{'overallRC': 300, 'modID': ModRCs['network'], 'rc': 300},
                {1: "Database operation failed, error: %(msg)s",
                 },
                "Operation on Network failed"
                ],
# Image Operation failed
    'image': [{'overallRC': 300, 'modID': ModRCs['image'], 'rc': 300},
              {1: "Database operation failed, error: %(msg)s",
               },
              "Operation on Image failed"
              ],
# Volume Operation failed
    'volume': [{'overallRC': 300, 'modID': ModRCs['volume'], 'rc': 300},
               {1: "Database operation failed, error: %(msg)s",
                },
               "Operation on Volume failed"
               ],
# Monitor Operation failed
    'monitor': [{'overallRC': 300, 'modID': ModRCs['monitor'], 'rc': 300},
                {1: "Database operation failed, error: %(msg)s",
                 },
                "Operation on Monitor failed"
                ],
# Invalid API name (Only used by sdk client/server)
# 'modID' would be set to ModRC['sdkserver'] or ModRC['sdkclient']
# 'rs' would also be set when get this error.
    'API': [{'overallRC': 400, 'modID': None, 'rc': 400},
            {},
            "Invalid API name"
            ],
# Object not exist
# Used when the operated object does not exist.
# 'modID' would be set to each module rc when raise the exception
# 'rs' is always 1
    'notExist': [{'overallRC': 404, 'modID': None, 'rc': 404},
                 {1: "Object '%(object)s' does not exist."},
                 "The operated object does not exist"
                 ],
# Conflict Error (The to-be-updated object status conflict)
    'conflict': [{'overallRC': 409, 'modID': None, 'rc': 409},
                 {},
                 "The operated object status conflict"
                 ],
# Object deleted.
# The operated object has been deleted and not exist any more.
# This can be used for some module that support deleted=1 in DB.
    'deleted': [{'overallRC': 410, 'modID': None, 'rc': 410},
                {},
                "The operated object is deleted"
                ],
# Internal error
# Module Internal error, rc is not defined here, it will be set when raising
# exception. when module id is not specified, the 'zvmsdk' module rc will be
# used.
    'internal': [{'overallRC': 500, 'modID': None, 'rc': 500},
                 {1: "Unexpected internal error in ZVM SDK, error: %(msg)s"},
                 "ZVM SDK Internal Error"
                 ],
    }

# smut internal error
# This const defines the list of smut errors that should be converted to
# internal error in SDK layer.
# Each element in the list is a tuple consisting the 'overallRC', 'rc',
# list of 'rs'
# when the value is 'None', it means always match.
SMUT_INTERNAL_ERROR = [(4, 4, range(1, 18)),
                       (2, 2, [99, ]),
                       (25, None, None),
                       (99, 99, [416, 417])
                       ]