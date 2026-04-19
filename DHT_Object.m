classdef DHT_Object
    %DHT_OBJECT This class is the OOP representation of one DHT layout
    %   Detailed explanation goes here
    
    properties
        complexityAxial = 5;
        complexityTangential = 5;
        lengthAxial = 0.15;
        radiusTangential = 0.1;
    end
    
    methods
        function obj = DHT_Object(inputArg1,inputArg2)
            %DHT_OBJECT Construct an instance of this class
            %   Detailed explanation goes here
            obj.Property1 = inputArg1 + inputArg2;
        end
        
        function outputArg = method1(obj,inputArg)
            %METHOD1 Summary of this method goes here
            %   Detailed explanation goes here
            outputArg = obj.Property1 + inputArg;
        end
    end
end

