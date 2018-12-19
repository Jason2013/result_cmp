OVERVIEW

  ShaderBench is a benchmark targeted to evaluate both shader compile time on CPU and execution time on GPU with top shaders captured from real games.

  For more detailed information, please refer to documentations under //depot/stg/PerfTools/Microbench/ShaderBench/doc/.


HOW TO RUN SHADERBENCh

  Prerequisites: 

  1.Make sure GPU/CPU frequency are fixed in order to reduce run-to-run variation. Refer to the following confluence page for details:
    http://confluence.amd.com/pages/viewpage.action?spaceKey=ASM&title=Microbench+Tips
  2.Install AMD graphics driver package (if drivers have already been installed, skip this step).
     E.g: To run tests on Vulkan API under Linux, you need to install Linux Vulkan driver first. Otherwise an error message like "
          Cannot find Vulkan loader libvulkan.so" will be output. For how to install Linux Vulkan driver, you can refer to
              http://confluence.amd.com/pages/viewpage.action?spaceKey=AMDGPU&title=amdgpu-pro+Installation+Instructions
          for details.
  3.Grab the formal ShaderBench release from \\gfxbench\Archive\Release
  4.Install the latest Vulkan SDK and make sure cube demo can run successfully
  5.OS dependency 
     a) DX11 tests can run on Win7 and Win10
     b) DX12 tests can only run on Win10
     c) Metal tests can only run on MacOS
     d) Vulkan/OpenGL tests can run on Win7,Win10 and Linux

  
  Two ways to run ShaderBench:

  1. Launch from Windows explorer
     First, please configure shaderbench options in ShaderBench.json to favor your requirements. Tips to configure most-frequently-used shaderbench options:

     a) Specify "TestCaseId=XXX" option in individual test's section to only run a list of particularly interested test cases, shaderbench will only 
        schedule test cases in the XXX list to run (XXX could be a single test case ID such as "1" or a list of test case ID such as "1, 2-5, 8", duplicate test 
        cases will be skipped and invalid test case ID, negative or larger than total test case numbers, will be ignored ).
     b) To dump rendered images, set "EnableDump=1" and specify image file through "DumpImageFileType" option and dump folder via "DumpDir" respectively. 
        Note: float/UNORM/SNORM format images can be dumped to BMP files; Integer format images can only be dumped to RAW image files.

  2. Launch from command line 
     ShaderBench can also be launched from command line with specified parameters overriding those pre-defined ones in ShaderBench.json config file. 
     E.g, 1) To only run test case #193:  
                shaderbench.exe -Global TestCaseId=193
          2) To run a specific test case based on test case name: 
                shaderbench.exe -Global TestCaseName=MadMax_spirv_Fs22_0xEAF9406B5683AD9A
          2) To run some test cases matching a specified naming pattern using wildcard: 
                shaderbench.exe -Global TestCaseName=MadMax_spirv_Fs*
  
  ShaderBench produces test result files along with a log file after benchmarking completes:
  - test_results.txt: Raw performance data including shader compile time and execution time
  - runlog.txt:       Runtime log file with detailed system information and runtime messages, which is very useful for debugging and postmortem diagnostics


USE SHADERBENCH

    Currently only Vulkan SPIRV shaders are supported in ShaderBench.

    RUN SHADERBENCH

    ShaderBench shares the same framework with Microbench, so if you're familiar with Microbench, using ShaderBench is simple.

    To run ShaderBench, just enter the folder where "shaderbench.exe" or "shaderbench" is, and in command line, type "shaderbench.exe" under Windows or "shaderbench" under Linux. After shaderbench
    finishes, check test_result.txt to see test results.

    There're many options in ShaderBench.json to control ShaderBench's behavior, you can modify them to meet your needs.

    Options in ShaderBench can also be specified via command line. Currently there're mainly two sections: Global section and ShaderTest section. To specify options, use the following syntax:
        shaderbench.exe -Global option1=value1, option2=value2, -ShaderTest option3=value3, option4=value4

    [TODO]: This piece of code needs to be improved for better user experience. Because "-ShaderTest" is redundant. But for now it's necessary.

    ADD SHADERS INTO SHADERBENCH

    1. To add a shader into ShaderBench, just edit ShaderList.json file. For example: there is a doom.spv to be ran, then just add the following into ShaderBench:

            "doom" : {
                "url" : "absolute_or_relative_path/doom.spv"
            }

        The test case name shown in test result for doom.spv above will be the string specified by "url", "doom" is the test case's group name.

        Sometimes you want to give it a more meaningful name, to do this, add a "name" property:

            "doom" : {
                "name" : "doom_top1_shader",
                "url" : "absolute_or_relative_path/doom.spv"
            }

        Then the test case name shown in test result for doom will be "doom_top1_shader".

    2. Wildcard '*' is supported in "url", which means to match any zero or more characters. For example, suppose all shaders from the game doom are dumped into "doom" folder. To run the shaders
       whose name contain "CS", just use:

            "doom" : {
                "url" : "absolute_or_relative_path/doom/*CS*.spv"
            }

       Similarly, "CS*" matches all names which start with "CS", "*CS" matches all names wich end with "CS".

       To get the '*''s content in a name, use %1, %2, ... to refer to the first, second, ..., '*''s content. For example:

            "doom" : {
                "name" : "%1ComputeShader%2",
                "url" : "absolute_or_relative_path/doom/*CS*.spv"
            }

        If in "doom" folder, there're two files doomV1_CS_0001.spv and doomV2_CS_0002.spv, then in test result there will be two test cases with name doomV1_ComputeShader_0001
        and doomV2_ComputeShader_0002 respectively.

       Wildcard in path is also supported. For example:

            "AllShaders" : {
                "name" : "%1ComputeShader%2",
                "url" : "absolute_or_relative_path/*/*CS*.spv"
            }

        Then all shaders in all subfolders (just top level sub folder) that match the pattern will be tested.

       To include all subfolders recursively, use more than one '*'. For example:

            "AllShaders" : {
                "name" : "%1ComputeShader%2",
                "url" : "absolute_or_relative_path/**/*CS*.spv"
            }

        Then all shaders in all subfolders (not just top level sub folder) that match the pattern will be tested.

        Note that the combination of wildcard is arbitrary. For example: "absolute_or_relative_path/**/doom/*LLPC*/2017/**/*CS*.spv" is valid.

    3. To let a test group contain more than one shaders, use the array syntax:

            "doom" : [
                {
                    "name" : "shader1",
                    "url" : "absolute_or_relative_path/shader1.spv"
                },
                {
                    "name" : "shader2",
                    "url" : "absolute_or_relative_path/shader2.spv"
                },
            ],
            "dota2" : [
                {
                    "name" : "shader1",
                    "url" : "absolute_or_relative_path/shader1.spv"
                },
                {
                    "name" : "shader2",
                    "url" : "absolute_or_relative_path/shader2.spv"
                },
            ]

        Then
           Test Group Name,      Test Name,     ...
            doom,                shader1,       ...
                                 shader2,       ...
            dota2,               shader1,       ...
                                 shader2,       ...

    4. Shader list in ShaderList.json can be grouped into a single json file, which means it can be orgnized in a hierarchy way. For example, existing ShaderList.json
       is grouped per game. That is, all shaders in a game is put into a GameName.json file. Then in ShaderList.json use "GameName" : "GameName.json" to run all shaders
       of the game.

    5. ShaderBench will create resources like images, framebuffer, ... in order to run shader. There're common macros defined in the "macro" section in ShaderList.json
       to control how they are created. For example, "SurfaceWidth" and "SurfaceHeight" is used to control framebuffer's width and height respectively. Sometimes there
       may be not suitable for a shader, then you can overwrite them for a test group or a test case. For example:

            // Default macros defined globally
           "macro" : {
            "SurfaceWidth" :            4096,
            "SurfaceHeight" :           4096,
            ...
            },

            "doom" : [
                {
                    // SurfaceWidth is 2048 for subsequent shaders in "doom" group, 4096 in global macro is overwritten
                    "macro" : {
                        "SurfaceWidth" :            2048,
                    }
                },
                {
                    "name" : "shader1",
                    "url" : "absolute_or_relative_path/shader1.spv" // 2048 is used
                },
                {
                    // SurfaceWidth is 1024 for this shader, 2048 in the group macro is overwritten
                    "macro" : {
                        "SurfaceWidth" :            1024,
                    },
                    "name" : "shader2",
                    "url" : "absolute_or_relative_path/shader2.spv"
                },
                {
                    "name" : "shader3",
                    "url" : "absolute_or_relative_path/shader3.spv" // 2048 is used
                },
                {
                    // SurfaceWidth is 512 for subsequent shaders in "doom" group, previous 2048 defined in gropu macro is overwritten
                    "macro" : {
                        "SurfaceWidth" :            512,
                    }
                },
                {
                    "name" : "shader4",
                    "url" : "absolute_or_relative_path/shader4.spv" // 512 is used
                },
            ],
            // Because no macro is re-defined in "dota2" group, all shaders in "dota2" group uses 4096.
            "dota2" : [
                {
                    "name" : "shader1",
                    "url" : "absolute_or_relative_path/shader1.spv"
                },
                {
                    "name" : "shader2",
                    "url" : "absolute_or_relative_path/shader2.spv"
                },
            ]

        In one word, macros are arranged in a hierarchy way, macro defined in test case level overwrite those defined in test group level, which overwrite those defined in global level; In the
        same level, macros defined later overwrite those defined eariler.


    GENERATE SOURCE CODE BY SHADERBENCH

    Currently only Vulkan is supported.

    1. Use RenderDoc to export a RenderDoc capture file (.rdc) to a .zip+xml format using "File->Export" menu.

    2. Get the latest shaderbench binary from http://ocltc:8111/viewType.html?buildTypeId=Microbench_MicrobenchBuilds_ShaderbenchWindows64bitRelease

    3. To generate source code, just use the following command line:
          shaderbench.exe -ShaderTest ShaderList=<your_zip_xml_file_path> SourceCodeGen.Enable=1
       By default the generated source is in the shaderbench.exe's folder. If you want to change it to another folder, append the following option:
          SourceCodeGen.OutputFolder=<your_local_folder>
